import { AnimatePresence, motion } from "framer-motion";
import type { Card as CardT, Decision } from "../api";
import Card from "./Card";
import CaughtUp from "./CaughtUp";

interface Props {
  cards: CardT[];
  caughtUp: boolean;
  hiddenCount: number;
  asOf: string;
  onFeedback: (card: CardT, decision: Decision) => void;
  onCta: (action: string) => void;
  onAskKate: (cardKey: string) => void;
}

export default function CardStack({ cards, caughtUp, hiddenCount, asOf, onFeedback, onCta, onAskKate }: Props) {
  return (
    <div className="feed">
      <div className="feed-head">
        <h2>For you</h2>
        <span>{cards.length} {cards.length === 1 ? "item" : "items"}</span>
      </div>
      <AnimatePresence initial={false} mode="popLayout">
        {cards.map((c) => (
          <motion.div
            key={c.card_key}
            layout
            initial={{ opacity: 0, y: 12, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, x: -80, scale: 0.96, transition: { duration: 0.22 } }}
            transition={{ type: "spring", stiffness: 380, damping: 32 }}
          >
            <Card card={c} asOf={asOf} onFeedback={onFeedback} onCta={onCta} onAskKate={onAskKate} />
          </motion.div>
        ))}
      </AnimatePresence>
      {(caughtUp || cards.length === 0) && (
        <motion.div layout key="caught-up">
          <CaughtUp hiddenCount={hiddenCount} empty={cards.length === 0} />
        </motion.div>
      )}
    </div>
  );
}
