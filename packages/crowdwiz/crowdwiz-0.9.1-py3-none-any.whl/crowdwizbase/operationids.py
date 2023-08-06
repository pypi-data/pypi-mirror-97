# -*- coding: utf-8 -*-
#: Operation ids
ops = [
	"transfer",
	"limit_order_create",
	"limit_order_cancel",
	"call_order_update",
	"fill_order",
	"account_create",
	"account_update",
	"account_whitelist",
	"account_upgrade",
	"account_transfer",
	"asset_create",
	"asset_update",
	"asset_update_bitasset",
	"asset_update_feed_producers",
	"asset_issue",
	"asset_reserve",
	"asset_fund_fee_pool",
	"asset_settle",
	"asset_global_settle",
	"asset_publish_feed",
	"witness_create",
	"witness_update",
	"proposal_create",
	"proposal_update",
	"proposal_delete",
	"withdraw_permission_create",
	"withdraw_permission_update",
	"withdraw_permission_claim",
	"withdraw_permission_delete",
	"committee_member_create",
	"committee_member_update",
	"committee_member_update_global_parameters",
	"vesting_balance_create",
	"vesting_balance_withdraw",
	"worker_create",
	"custom",
	"assert",
	"balance_claim",
	"override_transfer",
	"transfer_to_blind",
	"blind_transfer",
	"transfer_from_blind",
	"asset_settle_cancel",
	"asset_claim_fees",
	"fba_distribute",
	"bid_collateral",
	"execute_bid",
	"asset_claim_pool",
	"asset_update_issuer",
	"account_status_upgrade",

	"flipcoin_bet",
	"flipcoin_call",
	"flipcoin_win",
	"flipcoin_cancel",
	"flipcoin_loose",

	"lottery_goods_create_lot",
	"lottery_goods_buy_ticket",
	"lottery_goods_send_contacts",
	"lottery_goods_confirm_delivery",
	"lottery_goods_win",
	"lottery_goods_loose",

	"send_message",
	"matrix_open_room",
	"matrix_room_closed", 
	"matrix_cell_filled",

	"create_p2p_adv",
	"edit_p2p_adv",
	"clear_p2p_adv_black_list",
	"remove_from_p2p_adv_black_list",
	"create_p2p_order",
	"cancel_p2p_order",
	"autocancel_p2p_order",
	"autorefund_p2p_order",
	"call_p2p_order",
	"payment_p2p_order",
	"release_p2p_order",
	"open_p2p_dispute",
	"reply_p2p_dispute",
	"resolve_p2p_dispute",

	"lottery_goods_refund",
	"credit_system_get",
	"credit_total_repay",
	"credit_repay",
	"credit_offer_create",
	"credit_offer_cancel",
	"credit_offer_fill",
	"pledge_offer_give_create",
	"pledge_offer_take_create",
	"pledge_offer_cancel",
	"pledge_offer_fill",
	"pledge_offer_repay",
	"pledge_offer_auto_repay",

	"committee_member_update_gamezone_parameters",
	"committee_member_update_staking_parameters",
	"poc_vote",
	"poc_stak",
	"poc_staking_referal",
	"exchange_silver",
	"buy_gcwd",
	"approved_transfer_create",
	"approved_transfer_approve",
	"approved_transfer_cancel",
	"approved_transfer_open_dispute",
	"approved_transfer_resolve_dispute",
	"mass_payment",
	"mass_payment_pay",
]
operations = {o: ops.index(o) for o in ops}


def getOperationNameForId(i):
	""" Convert an operation id into the corresponding string
	"""
	for key in operations:
		if int(operations[key]) is int(i):
			return key
	return "Unknown Operation ID %d" % i


def getOperationName(id: str):
	""" This method returns the name representation of an operation given
		its value as used in the API
	"""
	if isinstance(id, str):
		# Some graphene chains (e.g. steem) do not encode the
		# operation_type as id but in its string form
		assert id in operations.keys(), "Unknown operation {}".format(id)
		return id
	elif isinstance(id, int):
		return getOperationNameForId(id)
	else:
		raise ValueError
