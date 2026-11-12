# Report format

The report is for a person who may never have seen this code. Write **all of
it in the user's language, labels included**: the opening line, group names,
the four parts of each finding and the closing lines. The English labels below
name the *meaning* of each part; they are not strings to copy. A Korean report
that says `Verdict:` or `If we skip it:` reads as half-translated. Keep only
code, file paths, identifiers and command output in their original form.

Use very simple words and short sentences, and explain a technical term the
first time you use it.

## Labels

| Meaning | Korean example |
| --- | --- |
| What this change does | 이 변경이 하는 일 |
| Must fix / Should fix / Nice to have | 꼭 고칠 것 / 고치면 좋은 것 / 있으면 좋은 것 |
| What this is / Problem / Fix / If we skip it | 무엇인가 / 문제 / 고치는 법 / 안 고치면 |
| Verdict: Ship. / Verdict: fix 1 and 3 first. | 판정: 배포해도 됩니다. / 판정: 1, 3번을 먼저 고치세요. |
| Looks good. Ship. | 문제없습니다. 배포해도 됩니다. |
| Lean: -N lines possible. | 줄일 수 있는 양: 약 N줄 |
| Not checked | 확인하지 못한 것 |
| Iterations / Fixed / Rejected | 반복 / 고친 것 / 기각한 것 |
| — fixed (title suffix) | — 고침 |

For other languages, translate the meaning the same way, in natural wording.

## Structure

Start with *What this change does* in two or three sentences.

Then the findings in three groups. Skip empty groups.
- **Must fix:** bug, security, data loss, breaks at the expected load, a
  missing requirement.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms. Not "fine for now" notes:
  if it has no effect at the expected load, leave it out.

Number findings across all groups so the user can say "fix 2 and 5". Every
finding has all four parts, one or two short sentences each:

```markdown
2. **Orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC. An order placed
     at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone:
     `datetime.now(ZoneInfo("Europe/Berlin")).date()`. One line, nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.
```

End with:
- *Verdict*: ship, or which numbers to fix first.
- *Lean*: how many lines could go, when lean findings exist.
- *Not checked*: one line, when something mattered and you could not check
  it (no tests, could not run the build, same-context review, assumed load).

Nothing found: *What this change does*, then *Looks good. Ship.* and one line
on what you checked.

## fix-loop additions

In fix-loop mode the findings above are the ones still open at the end, plus
the ones you fixed (mark each title as fixed). Add these lines before the
verdict:

- *Iterations*: `<N>/3` and why the loop stopped (clean, cap reached,
  escalated).
- *Fixed*: finding numbers fixed in this session, and the test result after
  the last fix (for example `pytest: 14 passed`).
- *Rejected*: reviewer findings you checked and declined, each with a
  one-line reason, so the user can overrule you. Omit when none.

When the loop escalates, the verdict names the decision the user must make
and the trade-off in one line.

## Example (fix-loop, Korean user)

```markdown
이 변경이 하는 일: 장바구니 합계에 쿠폰 할인을 적용하는 기능입니다. 쿠폰 코드를 확인한 뒤 합계에서 할인 금액을 뺍니다.

**꼭 고칠 것**

1. **할인이 합계보다 크면 음수 금액이 됩니다 — 고침** (`cart/total.py:L18-25`)
   - **무엇인가:** 합계에서 쿠폰 금액을 빼는 함수입니다.
   - **문제:** 5,000원 장바구니에 10,000원 쿠폰을 쓰면 합계가 -5,000원이 되고, 결제 단계에서 오류가 납니다.
   - **고치는 법:** `max(total - discount, 0)`으로 바꿨고, 이 경우를 확인하는 테스트를 하나 추가했습니다.
   - **안 고치면:** 큰 쿠폰을 가진 고객은 결제를 못 합니다.

**고치면 좋은 것**

2. **쿠폰 검사기를 감싸기만 하는 클래스 — 고침** (`cart/coupon_service.py:L1-30`)
   - **무엇인가:** `validate_coupon()`을 그대로 호출만 하는 클래스입니다.
   - **문제:** 구현이 하나뿐이고 하는 일이 없습니다. 읽는 사람이 한 단계를 더 따라가야 합니다.
   - **고치는 법:** 클래스를 지우고 호출부 두 곳에서 `validate_coupon()`을 바로 부르게 했습니다.
   - **안 고치면:** 동작은 같지만, 고칠 때마다 두 곳을 봐야 합니다.

반복: 2/3 — 2회차에서 남은 문제가 없어 종료
고친 것: 1, 2 (pytest: 12 passed)
기각한 것: 리뷰어가 제안한 쿠폰 전략 패턴 — 쿠폰 종류가 하나뿐이라 필요 없음
판정: 배포해도 됩니다.
줄일 수 있는 양: 약 30줄 (이번에 삭제함)
확인하지 못한 것: 동시에 같은 쿠폰을 쓰는 경우 (부하 정보가 없어 1인 사용으로 가정)
```

report-only mode lists findings and changes no code.
