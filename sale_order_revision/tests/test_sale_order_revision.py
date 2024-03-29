# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import Form

from odoo.addons.base_revision.tests import test_base_revision


class TestSaleOrderRevision(test_base_revision.TestBaseRevision):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.revision_model = cls.env["sale.order"]
        cls.partner = cls.env["res.partner"].create({"name": "Mr Odoo"})
        cls.product = cls.env["product.product"].create({"name": "Test product"})

    def _create_tester(self):
        sale_form = Form(self.revision_model)
        sale_form.partner_id = self.partner
        with sale_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return sale_form.save()

    @staticmethod
    def _revision_sale_order(sale_order):
        # Cancel the tester
        sale_order.action_cancel()
        # Create a new revision
        return sale_order.create_revision()

    def test_order_revision(self):
        sale_order_1 = self._create_tester()

        # Create a revision of the Sale Order
        self._revision_sale_order(sale_order_1)

        # Check the previous revision of the sale order
        revision_1 = sale_order_1.current_revision_id
        self.assertEqual(sale_order_1.state, "cancel")

        # Check the current revision of the sale order
        self.assertEqual(revision_1.unrevisioned_name, sale_order_1.name)
        self.assertEqual(revision_1.state, "draft")
        self.assertTrue(revision_1.active)
        self.assertEqual(revision_1.old_revision_ids, sale_order_1)
        self.assertEqual(revision_1.revision_number, 1)
        self.assertEqual(revision_1.name.endswith("-01"), True)
        self.assertEqual(revision_1.has_old_revisions, True)

        # Create a new revision of the Sale Order
        self._revision_sale_order(revision_1)
        revision_2 = revision_1.current_revision_id

        # Check the previous revision of the sale order
        self.assertEqual(revision_1.state, "cancel")
        self.assertFalse(revision_1.active)

        # Check the current revision of the sale order
        self.assertEqual(revision_2.unrevisioned_name, sale_order_1.name)
        self.assertEqual(revision_2, sale_order_1.current_revision_id)
        self.assertEqual(revision_2.state, "draft")
        self.assertTrue(revision_2.active)
        self.assertEqual(revision_2.old_revision_ids, sale_order_1 + revision_1)
        self.assertEqual(revision_2.revision_number, 2)
        self.assertEqual(revision_2.name.endswith("-02"), True)
        self.assertEqual(revision_2.has_old_revisions, True)

    def test_simple_copy(self):
        """Check copy process"""
        # Create a Sale Order
        sale_order_2 = self._create_tester()
        # Check the 'Order Reference' of the Sale Order
        self.assertEqual(sale_order_2.name, sale_order_2.unrevisioned_name)

        # Copy the Sale Order
        sale_order_3 = sale_order_2.copy()
        # Check the 'Order Reference' of the copied Sale Order
        self.assertEqual(sale_order_3.name, sale_order_3.unrevisioned_name)
