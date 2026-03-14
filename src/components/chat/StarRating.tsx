import React, { useState } from 'react';
import { Star } from 'lucide-react';
import { motion } from 'framer-motion';

interface Props {
    onSubmit: (rating: number) => void;
}

export const StarRating: React.FC<Props> = ({ onSubmit }) => {
    const [hover, setHover] = useState(0);
    const [selected, setSelected] = useState(0);
    const [submitted, setSubmitted] = useState(false);

    const handleSelect = (val: number) => {
        setSelected(val);
        setSubmitted(true);
        onSubmit(val);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-slate-900/50 border border-indigo-500/20 rounded-2xl p-6 mt-4 backdrop-blur-md shadow-lg"
        >
            <h4 className="text-sm font-bold text-indigo-200 mb-4 text-center">
                How was your experience with ZEDNY AI?
            </h4>

            {!submitted ? (
                <div className="flex items-center justify-center gap-3">
                    {[1, 2, 3, 4, 5].map((star) => (
                        <motion.button
                            key={star}
                            whileHover={{ scale: 1.2, rotate: 5 }}
                            whileTap={{ scale: 0.9 }}
                            onMouseEnter={() => setHover(star)}
                            onMouseLeave={() => setHover(0)}
                            onClick={() => handleSelect(star)}
                            className="focus:outline-none transition-transform"
                        >
                            <Star
                                className={`w-8 h-8 transition-all duration-300 ${(hover || selected) >= star
                                    ? 'fill-amber-400 text-amber-400 drop-shadow-[0_0_8px_rgba(251,191,36,0.5)]'
                                    : 'text-slate-600'
                                    }`}
                            />
                        </motion.button>
                    ))}
                </div>
            ) : (
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-2 space-y-2"
                >
                    <div className="w-12 h-12 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto mb-2 ring-1 ring-green-500/50">
                        <Star className="w-6 h-6 fill-green-400" />
                    </div>
                    <div className="text-white font-bold text-base">Thank you!</div>
                    <div className="text-xs text-indigo-300/60">Your feedback helps us grow.</div>
                </motion.div>
            )}
        </motion.div>
    );
};
