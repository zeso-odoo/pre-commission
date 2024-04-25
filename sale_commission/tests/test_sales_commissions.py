from odoo.tests.common import TransactionCase, tagged
from datetime import date

@tagged("post_install","-at_install")
class TestSaleCommission(TransactionCase):
    def setUp(self):
        super().setUp()
        self.sale_commission_model = self.env["sales.commissions"]
        self.account_move_model = self.env["account.move"]
        self.product_template_model = self.env["product.template"]
        self.product_category_model = self.env["product.category"]
        self.product_model = self.env["product.product"]
        self.user_model = self.env["res.users"]
        self.crm_team_model = self.env["crm.team"]

        self.product_category = self.product_category_model.create({"name": "Test category"})
        self.product = self.product_model.create({"name": "Test product"})
        self.product_template = self.product_template_model.create({"name": "Test product", "categ_id": self.product_category.id, "product_variant_id": self.product.id})
        self.salesperson = self.user_model.create({"name": "Test Salesperson", "login": "test_salesperson"})
        self.salesteam = self.crm_team_model.create({"name": "Test Sales Team"})

        self.sales_person_rule = self.commission_rule_model.create({
            "commission_rate": 10.0,
            "due_at": "invoicing",
            "commission_for": "salesperson",
            "product_category_id": self.product_category.id,
            "product_id" : self.product_template.id,
            "sales_person_id": self.salesperson.id,
        })

        self.sales_team_rule = self.commission_rule_model.create({
            "commission_rate": 10.0,
            "due_at": "invoicing",
            "commission_for": "salesteam",
            "product_category_id": self.product_category.id,
            "product_id" : self.product_template.id,
            "sales_team_id" : self.sales_team_id,
        })

        self.invoice = self.commission_rule_model.create({
            "date": date.today(),
            "invoice_date": date.today(),
            "invoice_user_id" : self.salesperson.id,
            "team_id": self.salesteam.id,
        })

        self.invoice_line = self.env["accoount.move"].create({
            "move_id": self.invoice.id,
            "product_id": self.product_template.product_variant_id.id,
            "quantity": 1,
            "price_unit": 100,
            "account_id": 1,
        })

    def test_create_sale_commission_sales_team(self):
        self.invoice.action_post()

        sale_commission = self.sale_commission_model.search([("invoice_id","=",self.invoice.id)])

        self.assertTrue(sale_commission)
        self.assertEqual(sale_commission.sales_team_id,self.sales_team)

    def test_open_form_view(self):
        self.invoice.action_post()

        sale_commission = self.sale_commission_model.search([("invoice_id","=",self.invoice.id)], limit=1)
        action = sale_commission.action_open_invoice_form()

        self.assertEqual(action["res_model","account.move"])
        self.assertEqual(action["res_id"],self.invoice.id)
