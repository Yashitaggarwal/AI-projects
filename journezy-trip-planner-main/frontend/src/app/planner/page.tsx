"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { motion } from "framer-motion";
import { Calendar, Users, Wallet, Plane, ShieldCheck, Baby, Accessibility } from "lucide-react";

// Types matching Backend
interface TripRequest {
    from_city: string;
    to_city: string;
    start_date: string;
    end_date: string;
    budget_amount: number;
    currency: string;
    travelers: {
        adults: number;
        children: number;
        seniors: number;
        children_under_5: number;
    };
    flight_preferences: {
        avoid_red_eye: boolean;
        avoid_early_morning: boolean;
        child_friendly: boolean;
        senior_friendly: boolean;
        direct_flights_only: boolean;
    };
    consider_toddler_friendly: boolean;
    consider_senior_friendly: boolean;
    safety_check: boolean;
    additional_instructions: string;
    language: string;
}

export default function PlannerPage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [step, setStep] = useState(1);

    const [formData, setFormData] = useState<TripRequest>({
        from_city: "",
        to_city: "",
        start_date: new Date().toISOString().split('T')[0],
        end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        budget_amount: 0,
        currency: "USD",
        travelers: {
            adults: 1,
            children: 0,
            seniors: 0,
            children_under_5: 0
        },
        flight_preferences: {
            avoid_red_eye: false,
            avoid_early_morning: false,
            child_friendly: false,
            senior_friendly: false,
            direct_flights_only: false
        },
        consider_toddler_friendly: false,
        consider_senior_friendly: false,
        safety_check: true,
        additional_instructions: "",
        language: "en"
    });

    const handleChange = (field: string, value: any) => {
        setFormData(prev => ({ ...prev, [field]: value }));
    };

    const handleTravelerChange = (field: string, value: number) => {
        setFormData(prev => ({
            ...prev,
            travelers: { ...prev.travelers, [field]: value }
        }));
    };

    const handleFlightPrefChange = (field: string, value: boolean) => {
        setFormData(prev => ({
            ...prev,
            flight_preferences: { ...prev.flight_preferences, [field]: value }
        }));
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
            // In a real app, use a proper state manager or URL params to pass data.
            // For this demo, we'll store in localStorage to persist across page loads.
            localStorage.setItem("tripRequest", JSON.stringify(formData));

            const response = await axios.post("/api/plan-trip", formData);
            localStorage.setItem("tripResult", JSON.stringify(response.data));

            router.push("/itinerary");
        } catch (error) {
            console.error("Planning failed", error);
            alert("Failed to plan trip. Please check specific inputs.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900 py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto">
                <div className="text-center mb-12">
                    <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white">Plan Your Trip</h1>
                    <p className="mt-2 text-lg text-slate-600 dark:text-slate-400">Tell us about your dream destination</p>
                </div>

                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-white dark:bg-slate-800 shadow-2xl rounded-3xl overflow-hidden"
                >
                    <div className="p-8 space-y-8">

                        {/* Section 1: Destination & Dates */}
                        <section className="space-y-4">
                            <h2 className="text-xl font-semibold flex items-center gap-2 text-blue-600 dark:text-blue-400">
                                <MapIcon className="w-5 h-5" /> Where & When
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <InputGroup label="From City" value={formData.from_city} onChange={(e) => handleChange("from_city", e.target.value)} placeholder="e.g. New York" />
                                <InputGroup label="To City" value={formData.to_city} onChange={(e) => handleChange("to_city", e.target.value)} placeholder="e.g. Paris" />

                                <InputGroup type="date" label="Start Date" value={formData.start_date} onChange={(e) => handleChange("start_date", e.target.value)} />
                                <InputGroup type="date" label="End Date" value={formData.end_date} onChange={(e) => handleChange("end_date", e.target.value)} />
                            </div>
                        </section>

                        <hr className="border-slate-200 dark:border-slate-700" />

                        {/* Section 2: Travelers */}
                        <section className="space-y-4">
                            <h2 className="text-xl font-semibold flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                                <Users className="w-5 h-5" /> Travelers
                            </h2>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <NumberInput label="Adults (18+)" value={formData.travelers.adults} onChange={(v) => handleTravelerChange("adults", v)} min={1} />
                                <NumberInput label="Children (5-17)" value={formData.travelers.children} onChange={(v) => handleTravelerChange("children", v)} />
                                <NumberInput label="Seniors (65+)" value={formData.travelers.seniors} onChange={(v) => handleTravelerChange("seniors", v)} />
                                <NumberInput label="Toddlers (<5)" value={formData.travelers.children_under_5} onChange={(v) => handleTravelerChange("children_under_5", v)} />
                            </div>
                        </section>

                        <hr className="border-slate-200 dark:border-slate-700" />

                        {/* Section 3: Budget & Preferences */}
                        <section className="space-y-4">
                            <h2 className="text-xl font-semibold flex items-center gap-2 text-teal-600 dark:text-teal-400">
                                <Wallet className="w-5 h-5" /> Budget & Preferences
                            </h2>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div className="flex gap-4">
                                    <div className="flex-1">
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Budget</label>
                                        <input type="number" value={formData.budget_amount} onChange={(e) => handleChange("budget_amount", parseFloat(e.target.value))} className="w-full p-3 rounded-xl border border-slate-200 dark:bg-slate-700 dark:border-slate-600" />
                                    </div>
                                    <div className="w-24">
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Currency</label>
                                        <select value={formData.currency} onChange={(e) => handleChange("currency", e.target.value)} className="w-full p-3 rounded-xl border border-slate-200 dark:bg-slate-700 dark:border-slate-600">
                                            <option>USD</option>
                                            <option>INR</option>
                                            <option>EUR</option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-3 pt-4">
                                <p className="text-sm font-medium text-slate-900 dark:text-white">Flight Preferences</p>
                                <div className="flex flex-wrap gap-3">
                                    <Checkbox label="Avoid Red Eye" checked={formData.flight_preferences.avoid_red_eye} onChange={(c) => handleFlightPrefChange("avoid_red_eye", c)} />
                                    <Checkbox label="Avoid Early Morning" checked={formData.flight_preferences.avoid_early_morning} onChange={(c) => handleFlightPrefChange("avoid_early_morning", c)} />
                                    <Checkbox label="Direct Flights Only" checked={formData.flight_preferences.direct_flights_only} onChange={(c) => handleFlightPrefChange("direct_flights_only", c)} />
                                </div>
                            </div>

                            <div className="space-y-3 pt-4">
                                <p className="text-sm font-medium text-slate-900 dark:text-white">Special Considerations</p>
                                <div className="flex flex-wrap gap-3">
                                    <Checkbox label="Toddler Friendly" icon={<Baby className="w-4 h-4" />} checked={formData.consider_toddler_friendly} onChange={(c) => handleChange("consider_toddler_friendly", c)} />
                                    <Checkbox label="Senior Friendly" icon={<Accessibility className="w-4 h-4" />} checked={formData.consider_senior_friendly} onChange={(c) => handleChange("consider_senior_friendly", c)} />
                                    <Checkbox label="Safety Check" icon={<ShieldCheck className="w-4 h-4" />} checked={formData.safety_check} onChange={(c) => handleChange("safety_check", c)} />
                                </div>
                            </div>
                        </section>

                        <div className="pt-6">
                            <button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="w-full py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg transform transition active:scale-95 disabled:opacity-70 flex justify-center items-center gap-2"
                            >
                                {loading ? "Generating Plan..." : "Generate Itinerary 🚀"}
                            </button>
                            {loading && <p className="text-center text-sm text-slate-500 mt-2 animate-pulse">This usually takes about 30-60 seconds due to AI processing...</p>}
                        </div>

                    </div>
                </motion.div>
            </div>
        </div>
    );
}

// Helpers
function InputGroup({ label, type = "text", value, onChange, placeholder }: any) {
    return (
        <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">{label}</label>
            <input
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-600 dark:bg-slate-700 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            />
        </div>
    )
}

function NumberInput({ label, value, onChange, min = 0 }: any) {
    return (
        <div>
            <label className="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1 uppercase tracking-wide">{label}</label>
            <input
                type="number"
                min={min}
                value={value}
                onChange={(e) => onChange(parseInt(e.target.value))}
                className="w-full p-2 rounded-lg border border-slate-200 dark:border-slate-600 dark:bg-slate-700 dark:text-white"
            />
        </div>
    )
}

function Checkbox({ label, checked, onChange, icon }: any) {
    return (
        <button
            onClick={() => onChange(!checked)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full border text-sm font-medium transition-all ${checked
                    ? 'bg-blue-100 border-blue-500 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300'
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50 dark:bg-slate-800 dark:border-slate-600 dark:text-slate-300'
                }`}
        >
            {icon} {label}
        </button>
    )
}

function MapIcon(props: any) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21" />
            <line x1="9" x2="9" y1="3" y2="18" />
            <line x1="15" x2="15" y1="6" y2="21" />
        </svg>
    )
}
