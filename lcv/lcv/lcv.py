from __future__ import unicode_literals
import frappe
from frappe import msgprint
from frappe.model.document import Document
from datetime import date
from frappe.utils import money_in_words,flt

@frappe.whitelist(allow_guest=True)
def updateJV(doc,method):
	account_list=[]
	account_json={}
	account_json["account"]="Expenses Included In Valuation - SHC"
	account_json["debit"]=doc.total_taxes_and_charges
	account_json["debit_in_account_currency"]=doc.total_taxes_and_charges
	account_json["cost_center"]=doc.cost_center
	account_list.append(account_json)
	for row in doc.taxes:
		account_json={}
		account_json["account"]=row.account
		account_json["credit"]=row.amount
		account_json["credit_in_account_currency"]=row.amount
		account_json["cost_center"]=row.cost_center
		account_list.append(account_json)

        jv = frappe.get_doc({
        "doctype": "Journal Entry",
        "posting_date": doc.invoice_date,
        "naming_series":"LC-JV-.YY.-.#",
        "voucher_type":"Journal Entry",
	"cost_center": doc.cost_center,
	"voucher_number":doc.name,
        "accounts":account_list
	})
        jv.insert(ignore_permissions=True)
        jv.submit()

@frappe.whitelist(allow_guest=True)
def UpdateLCV(doc,method):
	if doc.voucher_number:
		doc_jv = frappe.get_doc("Landed Cost Voucher", doc.voucher_number)
		doc_jv.jv = doc.name
		doc_jv.save()

@frappe.whitelist(allow_guest=True)
def cancelJV(doc,method):
        doc_jv = frappe.get_doc("Journal Entry", doc.jv)
        doc_jv.cancel()


@frappe.whitelist(allow_guest=True)
def dn(doc,method):
	if doc.total_qty >= doc.dn_qty and not doc.removed:
		for d in doc.items:
			if d.delivery_note:
			        doc_dn = frappe.get_doc("Delivery Note", d.delivery_note)
			        doc_dn.per_billed = 100
				doc_dn.status = 'Completed'
				doc_dn.save()
			if d.sales_order:
        		        doc_so = frappe.get_doc("Sales Order", d.sales_order)
	        	        doc_so.per_billed = 100
				doc_so.status = 'Completed'
        	        	doc_so.save()

	if doc.removed:
                for d in doc.items:
                        if d.delivery_note:
                                doc_dn = frappe.get_doc("Delivery Note", d.delivery_note)
				doc_dn.dn_qty = doc.dn_qty - doc.total_qty
                                doc_dn.save()
			if d.sales_order:
                                doc_so = frappe.get_doc("Sales Order", d.sales_order)
                                doc_so.per_billed = 100
                                doc_so.status = 'Completed'
                                doc_so.save()


@frappe.whitelist(allow_guest=True)
def getSP(customer):
	sp = frappe.db.sql("""select sales_person from `tabSales Team` where parent = '{0}';""".format(customer), as_list=1)
	return sp[0][0] if sp else 0.0

@frappe.whitelist(allow_guest=True)
def updateWords(doc,method):
	doc.words = money_in_words(doc.grand_total)


@frappe.whitelist()
def after_submit_sales_invoice(doc,method):
	for item in doc.items:
		if item.so_detail:
			billed_qty = frappe.db.get_value("Sales Order Item",item.so_detail,"billed_qty") + item.qty
			#frappe.msgprint("SQTY"+str(item.qty))
			#frappe.msgprint("BQTY"+str(billed_qty))
			frappe.db.set_value("Sales Order Item",item.so_detail,"billed_qty",billed_qty)

		if item.dn_detail:
			billed_qty = frappe.db.get_value("Delivery Note Item",item.dn_detail,"billed_qty") + item.qty
			#frappe.msgprint("DQTY"+str(item.qty))
			
			#frappe.msgprint("DBQTY"+str(billed_qty))
			frappe.db.set_value("Delivery Note Item",item.dn_detail,"billed_qty",billed_qty)

	for row in doc.items:
		if row.sales_order:
			so_doc = frappe.get_doc("Sales Order",row.sales_order)
			if not so_doc.status == "Completed":
				for row_item in so_doc.items:
					if row_item.qty >= row_item.delivered_qty and row_item.qty >= row_item.billed_qty:
						frappe.db.set_value("Sales Order",row.sales_order,"status","Completed")

		if row.delivery_note:
			dn_doc = frappe.get_doc("Delivery Note",row.delivery_note)
			if not dn_doc.status == "Completed":
				dn_status = False
				for row_item in dn_doc.items:
					frappe.msgprint(str(row_item.qty)+'-'+str(row_item.billed_qty))
					if row_item.qty <= row_item.billed_qty:
						dn_status = True
					else:
						dn_status = False
				if dn_status == True:
					frappe.db.set_value("Delivery Note",row.delivery_note,"status","Completed")


@frappe.whitelist()
def after_cancel_sales_invoice(doc,method):
	for item in doc.items:
		if item.so_detail:
			#frappe.msgprint("SQty"+str(item.qty))
			billed_qty = flt(frappe.db.get_value("Sales Order Item",item.so_detail,"billed_qty")) - item.qty
			#frappe.msgprint("SBQty"+str(billed_qty))
			frappe.db.set_value("Sales Order Item",item.so_detail,"billed_qty",billed_qty)

		if item.dn_detail:
			#frappe.msgprint("DQty"+str(item.qty))
			billed_qty = flt(frappe.db.get_value("Delivery Note Item",item.dn_detail,"billed_qty")) - item.qty
			#frappe.msgprint("DBQty"+str(billed_qty))
			frappe.db.set_value("Delivery Note Item",item.dn_detail,"billed_qty",billed_qty)

	for row in doc.items:
		if row.sales_order:
			so_doc = frappe.get_doc("Sales Order",row.sales_order)
			#if so_doc.status == "Completed":
			for row_item in so_doc.items:
				if row_item.qty < row_item.delivered_qty and row_item.qty < row_item.billed_qty:
					frappe.db.set_value("Sales Order",row.sales_order,"status","To Bill")

		if row.delivery_note:
			dn_doc = frappe.get_doc("Delivery Note",row.delivery_note)
			#if not dn_doc.status == "Completed":
			for row_item in dn_doc.items:
				if row_item.qty < row_item.billed_qty:
					frappe.db.set_value("Delivery Note",row.delivery_note,"status","To Bill")

@frappe.whitelist()
def assign_supplier_item_wise(doc,method):
	for item in doc.items:
		item.supplier = get_supplier(item.item_code) or ''


def get_supplier(item_code):
	supplier_data = frappe.db.sql("""select supplier from `tabItem Supplier` where parent=%s""",item_code)
	if len(supplier_data) >= 1:
		return supplier_data[0][0]
	else:
		return ''

@frappe.whitelist()
def after_submit_stock_entry_update(doc,method):
	if doc.voucher_type == "Sales Invoice":
		supplier = get_supplier(doc.item_code)
		frappe.db.set_value(doc.doctype,doc.name,"item_supplier",supplier)
		#frappe.db.sql("""update `tabStock Ledger Entry` set item_supplier=%s where item_code=%s""",(supplier,doc.item_code))