"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowLeft, Download, Plane, Hotel, MapPin, CalendarCheck } from "lucide-react";

export default function ItineraryPage() {
    const router = useRouter();
    const [result, setResult] = useState<any>(null);
    const [activeTab, setActiveTab] = useState("itinerary");

    useEffect(() => {
        // Retrieve data from local storage
        const storedResult = localStorage.getItem("tripResult");
        if (storedResult) {
            setResult(JSON.parse(storedResult));
        } else {
            router.push("/planner");
        }
    }, [router]);

    if (!result) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

    const { itinerary, document: markdownDoc } = result;

    // Safe accessors for nested data
    const flightsData = itinerary?.flights?.data || "No flight information available.";
    const hotelsData = itinerary?.hotels?.data || "No hotel information available.";
    const placesData = itinerary?.places?.data || "No places to visit information available.";
    const itineraryData = itinerary?.itinerary?.data || markdownDoc || "No itinerary generated.";

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900 pb-20">
            {/* Header */}
            <header className="bg-white dark:bg-slate-800 shadow-sm sticky top-0 z-30">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Link href="/planner" className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-full transition">
                            <ArrowLeft className="w-5 h-5 text-slate-600 dark:text-slate-300" />
                        </Link>
                        <h1 className="text-xl font-bold text-slate-900 dark:text-white">Your Trip Itinerary</h1>
                    </div>
                    <button className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition shadow-sm font-medium text-sm">
                        <Download className="w-4 h-4" /> Download PDF
                    </button>
                </div>
            </header>

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

                {/* Status Message */}
                {result.status !== "success" && (
                    <div className="bg-red-50 text-red-700 p-4 rounded-lg mb-6 border border-red-200">
                        {result.message}
                    </div>
                )}

                <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">

                    {/* Sidebar Navigation */}
                    <div className="lg:col-span-1 space-y-2">
                        <NavButton
                            active={activeTab === "itinerary"}
                            onClick={() => setActiveTab("itinerary")}
                            icon={<CalendarCheck className="w-5 h-5" />}
                            label="Day-by-Day Plan"
                        />
                        <NavButton
                            active={activeTab === "flights"}
                            onClick={() => setActiveTab("flights")}
                            icon={<Plane className="w-5 h-5" />}
                            label="Flights"
                        />
                        <NavButton
                            active={activeTab === "hotels"}
                            onClick={() => setActiveTab("hotels")}
                            icon={<Hotel className="w-5 h-5" />}
                            label="Hotels"
                        />
                        <NavButton
                            active={activeTab === "places"}
                            onClick={() => setActiveTab("places")}
                            icon={<MapPin className="w-5 h-5" />}
                            label="Places to Visit"
                        />
                    </div>

                    {/* Content Area */}
                    <div className="lg:col-span-3">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.3 }}
                            className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-lg min-h-[500px]"
                        >
                            {activeTab === "itinerary" && (
                                <div className="prose dark:prose-invert max-w-none">
                                    <h2 className="text-2xl font-bold mb-6 text-blue-600">Full Itinerary</h2>
                                    <div className="whitespace-pre-wrap font-sans text-sm leading-relaxed">
                                        {itineraryData}
                                    </div>
                                </div>
                            )}

                            {activeTab === "flights" && (
                                <div className="prose dark:prose-invert max-w-none">
                                    <h2 className="text-2xl font-bold mb-6 text-indigo-600">Flight Options</h2>
                                    <div className="whitespace-pre-wrap font-mono text-xs bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border border-slate-200 dark:border-slate-700">
                                        {flightsData}
                                    </div>
                                </div>
                            )}

                            {activeTab === "hotels" && (
                                <div className="prose dark:prose-invert max-w-none">
                                    <h2 className="text-2xl font-bold mb-6 text-indigo-600">Top Hotels</h2>
                                    <div className="whitespace-pre-wrap font-sans text-sm">
                                        {hotelsData}
                                    </div>
                                </div>
                            )}

                            {activeTab === "places" && (
                                <div className="prose dark:prose-invert max-w-none">
                                    <h2 className="text-2xl font-bold mb-6 text-teal-600">Must-Visit Places</h2>
                                    <div className="whitespace-pre-wrap font-sans text-sm">
                                        {placesData}
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    </div>

                </div>
            </main>
        </div>
    );
}

function NavButton({ active, onClick, icon, label }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium transition-all ${active
                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30'
                    : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700'
                }`}
        >
            {icon}
            {label}
        </button>
    )
}
