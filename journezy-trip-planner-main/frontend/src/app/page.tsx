"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { Plane, Map, Hotel, ArrowRight } from "lucide-react";

export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-900 dark:to-slate-800">

            <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex absolute top-10 px-10">
                <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
                    ✈️ Journezy Trip Planner
                </p>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-center space-y-8 max-w-3xl"
            >
                <h1 className="text-6xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400">
                    Design Your <br /> Dream Journey
                </h1>
                <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
                    Experience the power of AI-driven travel planning.
                    Curated itineraries, smart flight searches, and personalized recommendations
                    tailored just for you.
                </p>

                <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10">
                    <Link href="/planner">
                        <motion.button
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            className="px-8 py-4 bg-blue-600 text-white rounded-full font-bold shadow-lg hover:bg-blue-700 transition-all flex items-center justify-center gap-2"
                        >
                            Start Planning <ArrowRight className="w-5 h-5" />
                        </motion.button>
                    </Link>
                </div>
            </motion.div>

            <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
                {[
                    { icon: <Plane className="w-8 h-8 text-blue-500" />, title: "Smart Flights", desc: "Find the best connections tailored to your schedule." },
                    { icon: <Hotel className="w-8 h-8 text-indigo-500" />, title: "Curated Stays", desc: "Hotels and stays that match your style and budget." },
                    { icon: <Map className="w-8 h-8 text-teal-500" />, title: "AI Itineraries", desc: "Day-by-day plans optimized for your interests." }
                ].map((item, idx) => (
                    <motion.div
                        key={idx}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 + (idx * 0.1) }}
                        className="p-6 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-gray-100 dark:border-slate-700 hover:shadow-2xl transition-shadow"
                    >
                        <div className="mb-4 bg-slate-50 dark:bg-slate-700 p-3 w-fit rounded-xl">
                            {item.icon}
                        </div>
                        <h3 className="text-xl font-bold mb-2 dark:text-white">{item.title}</h3>
                        <p className="text-gray-500 dark:text-gray-400">{item.desc}</p>
                    </motion.div>
                ))}
            </div>
        </main>
    );
}
