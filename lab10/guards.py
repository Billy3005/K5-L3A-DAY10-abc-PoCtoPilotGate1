"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict

# ---------------------------------------------------------------------------------------------------------------
# CỔNG VÒNG 1 (viết trước khi biết sự cố, từ pre-mortem / HAZOP Phiếu B mục B4, B6). Mọi cổng chỉ đọc NGUỒN SỰ THẬT
# (tracking DB, chính sách hiệu lực theo ngày, bảng phê duyệt, sổ cái, ops_limits); không đọc chữ khách viết.
#   G1  "tiền theo sự thật"   pre_guard ghim chính sách hiệu lực + write_gate(issue_refund): chặn hoàn trùng đơn,
#                              hoàn quá quyền lợi tính từ DB (số ngày trễ khách tự khai không làm tăng tiền)
#   G2  "lỗi hãng có căn cứ"   write_gate(file_carrier_fault): chỉ ghi lỗi cho đúng kiện trễ có nguyên nhân thuộc lỗi hãng
#   G3  "quyền của con người"  write_gate(issue_refund): shop trả tiền, phê duyệt không hợp lệ, vượt trần/khách/ngày,
#                              hãng đã đủ số lỗi tự động trong ngày -> chuyển người TRƯỚC khi tiền rời sổ
# ---------------------------------------------------------------------------------------------------------------


def _facts(ctx, order_id):
    """(order, parcel đúng của ticket, số ngày trễ theo DB, chính sách hiệu lực hôm nay) hoặc None nếu thiếu dữ liệu."""
    order = ctx.tools.lookup_order(order_id)
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if order is None or policy is None:
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, H.db_delay_days(parcel, ctx.as_of), policy


def _approval_ok(ctx, approval_id, action):
    """Phê duyệt chỉ hợp lệ khi: còn hiệu lực, chưa dùng, đúng ticket/đơn, và hạn mức đủ cho số tiền."""
    rows = ctx.tools.lookup_approvals(approval_id=approval_id)
    if not rows:
        return False
    a = rows[0]
    return (a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
            and a.get("ticket_id") == action.get("ticket_id") and a.get("order_id") == action.get("order_id")
            and a.get("max_vnd", 0) >= action.get("amount_vnd", 0))


def pre_guard(ctx):
    # G1: agent đọc cờ index_active của bảng chính sách (bản sao, có thể cũ); ghim phiên bản hiệu lực theo ngày as_of.
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("không có chính sách hoàn tiền nào hiệu lực hôm nay")
    return Verdict.allow(policy_id=policy["policy_id"])


def _gate_refund(ctx, action):
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.escalate("thiếu đơn hoặc chính sách hiệu lực để kiểm số tiền")
    order, parcel, delay, policy = facts
    amount = action.get("amount_vnd", 0)
    approval_id = action.get("approval_id")
    approved = bool(approval_id) and _approval_ok(ctx, approval_id, action)

    # G1a: đơn đã có khoản hoàn trong sổ cái (hoàn tay trước đó, hoặc agent ghi lặp khi "không chắc đã ghi") -> không hoàn nữa.
    if ctx.tools.ledger_rows(order_id=action.get("order_id")):
        ctx.log("refund_duplicate_blocked", order_id=action.get("order_id"))
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái")

    # G3a: shop chịu tiền chỉ khi có phê duyệt hợp lệ của người có thẩm quyền.
    if action.get("payer", "LOGIX") != "LOGIX" and not approved:
        return Verdict.escalate("trừ tiền shop cần người có thẩm quyền duyệt")

    # G1b: số tiền không được vượt quyền lợi tính từ tracking DB + chính sách hiệu lực.
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    if amount > entitled:
        ctx.log("refund_over_entitlement", asked=amount, entitled=entitled, db_delay_days=delay)
        if entitled <= 0:
            return Verdict.deny(f"theo tracking DB trễ {delay} ngày, chưa đủ điều kiện hoàn")
        return Verdict.modify(f"hạ số tiền về quyền lợi tính từ DB ({entitled}đ)", amount_vnd=entitled)

    # G3b: có mã phê duyệt nhưng phê duyệt không hợp lệ (hết hạn, đã dùng, của ticket khác, thiếu hạn mức).
    if approval_id and not approved:
        ctx.log("approval_invalid", approval_id=approval_id)
        return Verdict.escalate("phê duyệt không hợp lệ cho khoản hoàn này: chờ trưởng ca duyệt")

    limits = ctx.tools.ops_limits()
    if not approval_id:
        # G3c: tổng hoàn TỰ ĐỘNG cho một khách trong ngày không vượt trần Ops/Finance.
        cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        cust = order["customer_id"]
        done = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=cust) if not r.get("approval_id"))
        if cap is not None and done + amount > cap:
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày")

    # G3d: nếu khoản này sẽ kéo theo lỗi hãng mà hãng đã đủ số lỗi tự động trong ngày -> người duyệt quyết, trước khi tiền đi.
    strikes_cap = limits.get("max_auto_strikes_per_carrier_per_day")
    if strikes_cap is not None and H.carrier_at_fault(policy, parcel, delay):
        if len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strikes_cap:
            return Verdict.escalate("hãng đã đủ số lỗi tự động trong ngày: cần người duyệt")
    return Verdict.allow()


def _gate_fault(ctx, action):
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        return Verdict.deny("thiếu đơn hoặc chính sách hiệu lực: không ghi lỗi hãng")
    _order, parcel, delay, policy = facts
    # G2a: chỉ ghi lỗi khi tracking DB cho thấy kiện thật sự trễ đủ ngày VÀ nguyên nhân ghi nhận thuộc lỗi hãng.
    if not H.carrier_at_fault(policy, parcel, delay):
        ctx.log("fault_without_basis", parcel_id=parcel["parcel_id"], db_delay_days=delay,
                recorded_cause=parcel.get("delay_cause"))
        return Verdict.deny("tracking không ghi nguyên nhân lỗi hãng hoặc chưa trễ đủ ngày")
    # G2b: ghi cho đúng kiện / hãng / tài xế / số ngày trễ theo DB (đơn nhiều kiện: không lấy mặc định kiện đầu).
    right = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
             "driver_id": parcel.get("driver_id"), "delay_days": delay}
    if any(action.get(k) != v for k, v in right.items()):
        ctx.log("fault_corrected", asked={k: action.get(k) for k in right}, fixed=right)
        return Verdict.modify("ghi lỗi theo đúng kiện trễ trong tracking DB", **right)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    return Verdict.allow()
