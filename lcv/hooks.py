# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "lcv"
app_title = "Lcv"
app_publisher = "Hardik Gadesha"
app_description = "App for passing LCV"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hardikgadesha@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lcv/css/lcv.css"
# app_include_js = "/assets/lcv/js/lcv.js"

# include js, css files in header of web template
# web_include_css = "/assets/lcv/css/lcv.css"
# web_include_js = "/assets/lcv/js/lcv.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "lcv.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "lcv.install.before_install"
# after_install = "lcv.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lcv.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Landed Cost Voucher": {
		"on_submit" : "lcv.lcv.lcv.updateJV",
		"on_cancel" : "lcv.lcv.lcv.cancelJV"
	},
	"Journal Entry":{
		"after_insert" : "lcv.lcv.lcv.UpdateLCV"
	},
	"Sales Invoice":{
		"validate" : "lcv.lcv.lcv.updateWords",
        "on_submit" : "lcv.lcv.lcv.after_submit_sales_invoice",
		"on_cancel": "lcv.lcv.lcv.after_cancel_sales_invoice",
		"on_update":"lcv.lcv.lcv.assign_supplier_item_wise"
    },
	"Stock Ledger Entry":{
		"on_submit" : "lcv.lcv.lcv.after_submit_stock_entry_update"
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"lcv.tasks.all"
# 	],
# 	"daily": [
# 		"lcv.tasks.daily"
# 	],
# 	"hourly": [
# 		"lcv.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lcv.tasks.weekly"
# 	]
# 	"monthly": [
# 		"lcv.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "lcv.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lcv.event.get_events"
# }

