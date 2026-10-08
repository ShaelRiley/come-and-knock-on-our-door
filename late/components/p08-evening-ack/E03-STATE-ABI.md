# ACK kernel state and public API

Selector 2991 is `h8E`; 2992–2999 remain reserved and unallocated. Existing selector values and class owners are unchanged. This adds five vocabulary bytes: 34,881 → 34,886. Main remains 64,348 bytes; all code changes are in owner 989.

Public queries retain their original allocation: 2935 `h8ActorRoom`, 2936 `h8EveningCommitted`, 2937 `h8EveningReady`. ActorRoom is unchanged. Committed validates the durable completed literal history and its historical I/O witness without querying current input/restore barriers or repairing anything. Ready always returns false in this slice. The complete transition and final-room transaction remain disabled.

`h8E` commands are 0 stable deferred ACK service, 1 explicit publication retry arm after the existing native Yes consumes its consent descriptor, 2 strict raw saved-state validation, 3 pure committed-history query, and 5 retire the attempt latch. Other commands return zero. A direct arm never creates storage authority; service still requires the exact live successful I/O receipt and a stable ordinary scene boundary.

Private `h8EW[48]` is the durable witness:

- 0: phase, 0 absent or 1 committed awaiting explicit cut
- 1: schema 1
- 2–30: exact historical `h8IO[29]` whose state was 4 and native result bit was 1
- 31–38: completed request, requested-at, checklist and confirmation serial pairs, matching literal words 24–31
- 39–40: literal ACK revision, exactly one unsigned 32-bit increment after the successful I/O revision and equal to ONCE_EVENING
- 41–46: system doc 1013, transition doc 1017, system first row 1129/count 1, transition first row 1134/count 4
- 47: unread transition mask, zero throughout this slice

`h8EP[48]` prepares the full proposed witness and must be zero at every saved boundary. `h8EC[3]` holds attempted I/O generation high/low and a one-attempt latch. A precommit refusal retains the successful live I/O receipt and pending domain request, with no domain, actor, owner or visible-output publication. Frame ticks cannot retry that attempt. Existing Begin can rearm its publication; this uses the same successful receipt and makes no new SaveGame call. Not Yet still cancels the request. Ordinary restoration retires the attempt latch and current I/O authority; any pre-ACK restored request requires the existing explicit storage retry.

The known document rows, their static backing and two-document queue capacity prepare before the unchanged literal ACK method stages its candidate. Candidate output and every proposed witness/queue/owner/preparation/actor field are checked before `h8CommitReserved`. The private witness is published synchronously under the same critical guard. The saved output is private unread intent; it is not appended to the visible reader queue before actual actors can be staged. No Graph12/page/audio receipt is emitted here.

The strict phase-1 restore guard additionally requires the unchanged meeting route and epoch, current generation and readiness group peers, exact current ACK revision, actual actor rooms, empty transient preparation, and drained reader queue. It runs before older inventory publishers. Ordinary save/restore remains available despite the phase-1 gameplay action barrier. Invalid raw admission rejects and permits existing whole-campaign recovery.

The later presentation gate must reserve new phase-specific raw admission before changing actors; it must not retain the first slice's exact current-revision/meeting checks as an accidental permanent ban on future legitimate actions. It will keep the historical witness immutable while separately tracking explicit cut, actual staging, text presentation and final handoff. Unread canonical text must remain resumable through the existing reader. This packet claims no native filesystem, wildcard, actor pixel, listening or controller acceptance.
