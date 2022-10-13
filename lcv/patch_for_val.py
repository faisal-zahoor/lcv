from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_url


@frappe.whitelist()
def update_val_rate_in_sales_invoice():
	invoice = frappe.get_all("Sales Invoice",filters={"docstatus":1},fields=["name"])
	for item in invoice:
		if item.name:
			inv_doc = frappe.get_doc("Sales Invoice",item.name)
			for row in inv_doc.items:
				val_rate = frappe.db.sql("""select sum(stock_value)/sum(qty_after_transaction) from `tabStock Ledger Entry` where item_code=%s
						and (warehouse = 'Store - Shuwaikh - SB' or warehouse = 'Ahmadi S/R - SB'
						or warehouse = 'Decor - Shuwaikh - SB' or warehouse = 'Main SB - SB' or warehouse = 'Shuwaikh S/R - SB')
						and is_cancelled='No'
						order by posting_date desc, posting_time desc, name desc""",row.item_code)
				if len(val_rate) >= 1:
					val_rate = val_rate[0][0] or 0
				else:
					val_rate = 0
				frappe.db.sql("""update `tabSales Invoice Item` set val_rate=%s where name=%s""",(val_rate,row.name))