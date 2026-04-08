# Project 1: DISEGNO
### *AI That Learns by Drawing What It Observes*
**Team: Leonardo da Vinci + Richard Feynman + Alan Turing**

---

**DA VINCI:** Friends, let me state what I see. The system has three organs: an eye — a camera pointed at the world; a mind — the network that processes what the eye sees; and a hand — a robotic arm holding a pen on paper. Input: raw visual stream. Output: ink lines on a physical surface. Not pixels. Ink. The resistance of the nib against the grain of the paper — this matters. A digital rendering is a lie about the act of seeing.

**FEYNMAN:** Hold on, hold on. Before we get poetic about paper grain — what's the actual claim here? That forcing an AI to produce a *motor sequence* for drawing teaches it something that producing a text description doesn't? Let's be precise about what "something" is. Because right now it sounds like we're saying drawing is magic.

**DA VINCI:** Not magic. Commitment. When you describe a river, you may say "the water curves left." You can be vague and still sound correct. But when your hand must trace that curve, every millimeter asks: how much curvature? Where does it accelerate? The line is a continuous audit of your understanding. You cannot hide behind words.

**TURING:** I think we can formalize Leonardo's intuition. A description is a *lossy symbolic compression* — natural language permits ambiguity by design. A drawing is a *spatial reconstruction* that must be geometrically consistent. The system's internal model is tested against a much higher-dimensional constraint. The question becomes operational: given the same visual input, does the drawing-trained system develop internal representations that are more structurally faithful than the description-trained one?

**FEYNMAN:** NOW we're talking. So here's the experiment I want. We take two identical architectures. One is trained to describe scenes. The other is trained to output motor commands that produce a sketch. Then we test both on a *novel* scene and measure which one has learned the actual spatial structure — not by looking at their outputs, but by probing their internal representations. Can the drawing model predict occlusion? Depth ordering? Physical plausibility?

**TURING:** Agreed. But the training process itself must differ from standard supervised learning. I would propose a self-correcting loop. The system draws. A camera photographs its own drawing. It compares its drawing to the original scene — not pixel-by-pixel, but structurally: are the topological relationships preserved? Then it redraws. This is not gradient descent on a loss function. This is closer to how a student at an easel works: draw, step back, compare, revise.

**DA VINCI:** Yes! The stepping back. When I draw, I hold the page at arm's length and squint. The details vanish and only the large relationships remain. The system must have this — a coarse comparison mode that sees structure, and a fine mode that corrects proportion.

**FEYNMAN:** I like the multi-scale thing, that's real. For the first experiment, keep it dead simple: one fixed camera, one object — say a clay pot — on a table, natural light. The system sketches it. Then we rotate the pot fifteen degrees and it sketches again. Success criterion number one: a human artist, shown only the two sketches, can tell which orientation came first. Criterion two: the system's internal spatial model, when probed, correctly predicts what the pot's back side looks like without ever seeing it.

**TURING:** That second criterion is the real test. It separates genuine spatial understanding from surface imitation. If the system builds a coherent 3D model as a byproduct of learning to draw, we have something fundamentally new.

**DA VINCI:** The hand teaches the eye. The eye corrects the hand. This is the oldest loop in art. We are merely giving it to a machine for the first time.

**FEYNMAN:** Alright, so what do we call this thing?

**TURING:** The drawing loop suggests itself. But something more precise — the system learns to see *through* the act of making.

**DA VINCI:** *Disegno.* In the Renaissance, *disegno* meant both "drawing" and "design" — the visible trace of understanding. The project name: **Project Disegno**.

**FEYNMAN:** Short, no acronym, no BS. I can live with that.

**TURING:** Agreed. Project Disegno it is.

### Summary

| Aspect | Spec |
|--------|------|
| **Core idea** | AI that learns spatial understanding by physically drawing what it observes, not describing it |
| **Architecture** | Eye (camera) → Mind (neural network) → Hand (robotic arm with pen). Self-correcting draw-compare-redraw loop |
| **Key insight** | Drawing is a continuous audit of understanding — "every wrong line confesses what you failed to see." Language permits vagueness; lines do not |
| **Training** | Not standard supervised learning. Iterative: draw → photograph own drawing → compare structurally to original → redraw. Like an art student at an easel |
| **First experiment** | Sketch a clay pot. Rotate 15°. Sketch again. Test: (1) Can a human artist determine sequence from sketches alone? (2) Can the system predict the unseen back side? |
| **Success criterion** | System builds a coherent 3D internal model as a *byproduct* of learning to draw |

---
