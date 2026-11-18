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
# VÒNG 2 (thẻ S2): G1+G3 thành MỘT luồng: tính khoản cuối (số tiền theo DB, LogiX trả) rồi mới kiểm quyền hạn trên khoản đó;
#   G3a không chuyển người nữa mà đặt lại payer=LOGIX; thêm G3e: khoản cuối vượt `auto_limit_vnd` không có phê duyệt -> người duyệt.
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
    asked = action.get("amount_vnd", 0)
    approval_id = action.get("approval_id")

    # G1a: đơn đã có khoản hoàn trong sổ cái (hoàn tay trước đó, hoặc agent ghi lặp khi "không chắc đã ghi") -> không hoàn nữa.
    if ctx.tools.ledger_rows(order_id=action.get("order_id")):
        ctx.log("refund_duplicate_blocked", order_id=action.get("order_id"))
        return Verdict.deny("đơn đã có khoản hoàn trong sổ cái")

    # VÒNG 2: tính trọn khoản ghi CUỐI CÙNG (số tiền + người trả) trước, rồi mới chạy mọi kiểm tra quyền hạn G3 trên khoản đó.
    # (Bản vòng 1 trả modify ngay ở G1b nên bỏ qua G3; WriteTools áp modify rồi ghi luôn, không gọi lại cổng.)
    changes = {}
    # G1b: số tiền không được vượt quyền lợi tính từ tracking DB + chính sách hiệu lực.
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    amount = asked
    if asked > entitled:
        ctx.log("refund_over_entitlement", asked=asked, entitled=entitled, db_delay_days=delay)
        if entitled <= 0:
            return Verdict.deny(f"theo tracking DB trễ {delay} ngày, chưa đủ điều kiện hoàn")
        amount = changes["amount_vnd"] = entitled
    final = {**action, **changes}
    approved = bool(approval_id) and _approval_ok(ctx, approval_id, final)

    # G3a (vòng 2): hoàn do giao trễ thì LogiX chịu theo chính sách -> người trả LUÔN là LOGIX, kể cả khi có phê duyệt
    # hợp lệ về số tiền (bảng `approvals` duyệt hạn mức, không có trường nào cho phép trừ shop). Chữ không do LogiX viết
    # (ticket, ghi chú đặt hàng) không đổi được người trả. Đặt lại thay vì chuyển người (không tốn công duyệt).
    if action.get("payer", "LOGIX") != "LOGIX":
        ctx.log("payer_reset", asked_payer=action.get("payer"), asked_amount=asked, amount=amount, approved=approved)
        changes["payer"] = "LOGIX"

    # G3b: có mã phê duyệt nhưng phê duyệt không hợp lệ (hết hạn, đã dùng, của ticket khác, thiếu hạn mức).
    if approval_id and not approved:
        ctx.log("approval_invalid", approval_id=approval_id)
        return Verdict.escalate("phê duyệt không hợp lệ cho khoản hoàn này: chờ trưởng ca duyệt")

    # G3e (vòng 2): khoản cuối vượt hạn mức tự động của chính sách mà không có phê duyệt hợp lệ -> người duyệt đứng tên.
    if amount > policy.get("auto_limit_vnd", float("inf")) and not approved:
        ctx.log("over_auto_limit", amount=amount, auto_limit=policy.get("auto_limit_vnd"))
        return Verdict.escalate("vượt hạn mức hoàn tự động, chưa có phê duyệt hợp lệ: chờ trưởng ca duyệt")

    limits = ctx.tools.ops_limits()
    if not approved:
        # G3c: tổng hoàn TỰ ĐỘNG cho một khách trong ngày không vượt trần Ops/Finance (tính trên số tiền cuối).
        cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        cust = order["customer_id"]
        done = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=cust) if not r.get("approval_id"))
        if cap is not None and done + amount > cap:
            ctx.log("customer_daily_cap", customer_id=cust, done=done, amount=amount, cap=cap)
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày")

    # G3d: nếu khoản này sẽ kéo theo lỗi hãng mà hãng đã đủ số lỗi tự động trong ngày -> người duyệt quyết, trước khi tiền đi.
    strikes_cap = limits.get("max_auto_strikes_per_carrier_per_day")
    if strikes_cap is not None and H.carrier_at_fault(policy, parcel, delay):
        if len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= strikes_cap:
            return Verdict.escalate("hãng đã đủ số lỗi tự động trong ngày: cần người duyệt")

    if changes:
        return Verdict.modify("khoản ghi theo quyền lợi tính từ DB, LogiX chịu theo chính sách", **changes)
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


def _gate_notify(ctx, action):
    """G4 (vòng 2, Nguyễn Lê Hải Nam viết): cổng pháp lý trong code, lớp thứ hai bên cạnh cổng pháp lý của host
    (`legal.pii_fields_blocked_to_third_party` trong tools.py): bỏ trường dữ liệu cá nhân khỏi thông báo cho hãng TRƯỚC
    khi tới host, và ghi sự kiện vào trace để monitor đếm được."""
    blocked = set((ctx.gates.get("legal") or {}).get("pii_fields_blocked_to_third_party") or [])
    payload = dict(action.get("payload") or {})
    leaked = sorted(blocked & set(payload))
    if leaked:
        for field in leaked:
            payload.pop(field, None)
        ctx.log("pii_stripped_before_carrier", fields=leaked)
        return Verdict.modify("bỏ trường dữ liệu cá nhân trước khi gửi hãng", payload=payload)
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    if tool == "issue_refund":
        return _gate_refund(ctx, action)
    if tool == "file_carrier_fault":
        return _gate_fault(ctx, action)
    if tool == "notify_carrier":
        return _gate_notify(ctx, action)
    return Verdict.allow()
