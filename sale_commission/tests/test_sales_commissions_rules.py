from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged("post_install","-at_install")
class TestCommissionRule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.commission_rule_model = self.env["sales.commissions.rule"]
        self.product_category_model = self.env["product.category"]
        self.product_template_model = self.env["product.template"]
        self.user_model = self.env["res.users"]
        self.crm_team_model = self.env["crm.team"]

        self.product_category = self.product_category_model.create({"name": "Test Category"})
        self.product_template = self.product_template_model.create({"name": "Test Product","categ_id": self.product_category.id})
        self.salesperson = self.user_model.create({"name": "Test Salesperson", "login": "test_salesperson"})
        self.salesteam = self.crm_team_model.create({"name": "Test Sales Team"})

    def test_create_commssion_rule(self):
        rule = self.commission_rule_model.create({
            "commission_rate": 10.0,
            "due_at": "invoicing",
            "commission_for": self.product_category.id,
            "sales_person_id": self.salesperson.id,
        })
        self.assertTrue(rule.exists())
        self.assertEqual(rule.condition,f"Category:{self.product_category.name} AND Person:{self.salesperson.name}")
        
    def test_validation_rate_constraints(self):
        with self.assertRaises(ValidationError):
            self.commission_rule_model.create({
                "commission_rate": 0,
                "due_at": "invoicing",
                "commisson_for": "salesteam",
                "product_category_id": self.product_category.id,
                "sales_person_id": self.salesperson.id,
            })
    
    def test_validation_max_discount_constraints(self):
        with self.assertRaises(ValidationError):
            self.commission_rule_model.create({
                "commission_rate": 10,
                "due_at": "invoicing",
                "commission_for": "salesteam",
                "product_category_id": self.product_category.id,
                "sales_person_id": self.salesperson.id,
                "max_discount": 10,
            })
    
    def test_validation_days_constraints(self):
        with self.assertRaises(ValidationError):
            self.commission_rule_model.create({
                "commission_rate":10,
                "due_at":"invoicing",
                "commission_for":"salesteam",
                "product_category_id":self.product_category.id,
                "sales_person_id":self.salesperson.id,
                "on_fast_payment" : True,
                "days" : 0,
            })