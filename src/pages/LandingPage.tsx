import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
    Sparkles, ArrowRight, Zap, Shield, Globe,
    MessageSquare, Cpu, BarChart
} from 'lucide-react';

const LandingPage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-hero-gradient text-slate-50 font-sans overflow-hidden">
            {/* Navbar */}
            <nav className="fixed top-0 w-full z-50 bg-[#0f172a]/40 backdrop-blur-2xl border-b border-white/5 shadow-soft transition-all duration-300">
                <div className="container mx-auto px-6 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
                            <Sparkles className="w-5 h-5 text-white" />
                        </div>
                        <span className="text-2xl font-display font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-100 to-slate-400 tracking-wide">
                            ZEDNY.AI
                        </span>
                    </div>
                    <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
                        <a href="#features" className="hover:text-white transition-colors">Features</a>
                        <a href="#solutions" className="hover:text-white transition-colors">Solutions</a>
                        <a href="#pricing" className="hover:text-white transition-colors">Pricing</a>
                    </div>
                    <button
                        onClick={() => navigate('/chat')}
                        className="px-6 py-2.5 bg-white/10 text-white border border-white/20 font-medium rounded-full hover:bg-white hover:text-slate-900 transition-all duration-300 text-sm shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.3)] backdrop-blur-md"
                    >
                        Try Demo
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 px-6">
                {/* Background Blobs */}
                <div className="absolute top-[-10%] left-1/2 -translate-x-1/2 w-[800px] h-[800px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 animate-pulse-slow" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[600px] h-[600px] bg-purple-600/20 rounded-full blur-[120px] -z-10" />
                <div className="absolute top-[20%] right-[10%] w-[300px] h-[300px] bg-pink-500/10 rounded-full blur-[90px] -z-10 animate-pulse-slow" />

                <div className="container mx-auto text-center max-w-4xl">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                    >
                        <span className="inline-block px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium mb-6">
                            Next Generation Enterprise AI 🚀
                        </span>
                        <h1 className="text-5xl md:text-7xl font-display font-bold tracking-tight mb-8 leading-[1.15]">
                            The Intelligent Brain for <br />
                            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 drop-shadow-sm">
                                Modern Businesses
                            </span>
                        </h1>
                        <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
                            Experience the future of customer interaction. Zedny AI combines advanced natural language processing with real-time analytics to solve problems faster than ever.
                        </p>
                        <div className="flex flex-col md:flex-row items-center justify-center gap-4">
                            <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => navigate('/chat')}
                                className="w-full md:w-auto px-8 py-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-600 bg-[length:200%_auto] hover:bg-[position:right_center] text-white rounded-2xl font-semibold text-lg shadow-glow-lg flex items-center justify-center gap-2 group transition-all duration-500"
                            >
                                Start Free Trial
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </motion.button>
                            <button className="w-full md:w-auto px-8 py-4 bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 text-white rounded-2xl font-semibold text-lg backdrop-blur-xl transition-all duration-300 shadow-glass">
                                Watch Demo
                            </button>
                        </div>
                    </motion.div>
                </div>
            </section>

            {/* Features Grid */}
            <section className="py-24 bg-[#0F172A]/50 border-t border-white/5" id="features">
                <div className="container mx-auto px-6">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-5xl font-display font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">Powerful Capabilities</h2>
                        <p className="text-slate-400 text-lg">Everything you need to automate and enhance your workflow.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            {
                                icon: <MessageSquare className="w-6 h-6 text-blue-400" />,
                                title: "Adaptive Chat",
                                desc: "Understands context, tone, and intent to provide human-like responses.",
                                color: "bg-blue-500/10"
                            },
                            {
                                icon: <Zap className="w-6 h-6 text-amber-400" />,
                                title: "Instant Analysis",
                                desc: "Processes complex queries in milliseconds using advanced RAG pipelines.",
                                color: "bg-amber-500/10"
                            },
                            {
                                icon: <Globe className="w-6 h-6 text-green-400" />,
                                title: "Multi-Language",
                                desc: "Native support for Arabic and English with automatic dialect detection.",
                                color: "bg-green-500/10"
                            }
                        ].map((feature, i) => (
                            <motion.div
                                key={i}
                                whileHover={{ y: -8 }}
                                className="p-8 rounded-[2rem] bg-white/5 border border-white/5 hover:border-indigo-500/30 hover:bg-white/[0.08] transition-all duration-500 group shadow-soft backdrop-blur-md"
                            >
                                <div className={`w-12 h-12 rounded-2xl ${feature.color} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                                    {feature.icon}
                                </div>
                                <h3 className="text-2xl font-display font-semibold mb-3 tracking-wide">{feature.title}</h3>
                                <p className="text-slate-400 leading-relaxed text-sm md:text-base">{feature.desc}</p>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Bento Grid Visuals */}
            <section className="py-24 px-6">
                <div className="container mx-auto">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 h-auto md:h-[600px]">
                        {/* Large Card */}
                        <div className="lg:col-span-2 bg-gradient-to-br from-indigo-900/40 to-[#0F172A] border border-indigo-500/20 rounded-3xl p-8 relative overflow-hidden flex flex-col justify-end group">
                            <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=2565&auto=format&fit=crop')] bg-cover bg-center opacity-20 mix-blend-overlay transition-opacity group-hover:opacity-30" />
                            <div className="absolute top-4 right-4 p-2 bg-black/40 backdrop-blur rounded-lg border border-white/10">
                                <Cpu className="w-6 h-6 text-indigo-300" />
                            </div>
                            <div className="relative z-10 p-4">
                                <h3 className="text-4xl font-display font-bold mb-3 tracking-tight">Neural Processing Core</h3>
                                <p className="text-slate-300/80 max-w-lg text-lg leading-relaxed">Our proprietary model architecture ensures 99.9% uptime and enterprise-grade security for your data, processing millions of requests seamlessly.</p>
                            </div>
                        </div>

                        {/* Tall Card */}
                        <div className="bg-[#0f172a]/80 border border-white/5 rounded-3xl p-8 flex flex-col relative overflow-hidden shadow-soft backdrop-blur-lg">
                            <div className="absolute top-0 right-0 w-40 h-40 bg-purple-500/10 rounded-full blur-[60px]" />
                            <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center mb-6 text-purple-400">
                                <BarChart className="w-6 h-6" />
                            </div>
                            <h3 className="text-2xl font-display font-bold mb-2">Real-time Insights</h3>
                            <p className="text-slate-400 mb-8">Track user sentiment and engagement metrics live.</p>

                            {/* Visual Placeholder */}
                            <div className="flex-1 bg-white/5 rounded-2xl border border-white/5 relative overflow-hidden">
                                <div className="absolute inset-0 flex items-center justify-center">
                                    <div className="flex gap-2 items-end h-32">
                                        <div className="w-4 bg-indigo-500/40 h-16 rounded-t-sm" />
                                        <div className="w-4 bg-indigo-500/60 h-24 rounded-t-sm" />
                                        <div className="w-4 bg-indigo-500/80 h-20 rounded-t-sm" />
                                        <div className="w-4 bg-indigo-500 h-28 rounded-t-sm" />
                                        <div className="w-4 bg-purple-500 h-12 rounded-t-sm" />
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Small Card 1 */}
                        <div className="bg-gradient-to-br from-[#0f172a]/90 to-indigo-900/10 border border-white/5 rounded-3xl p-8 shadow-soft backdrop-blur-lg">
                            <Shield className="w-8 h-8 text-emerald-400 mb-4 drop-shadow-[0_0_10px_rgba(52,211,153,0.5)]" />
                            <h3 className="text-xl font-display font-bold mb-2">Enterprise Secure</h3>
                            <p className="text-slate-400 text-sm">GDPR & SOC2 Compliant infrastructure.</p>
                        </div>

                        {/* Small Card 2 */}
                        <div className="lg:col-span-2 bg-gradient-to-r from-indigo-900/30 to-[#0f172a] border border-white/5 rounded-3xl p-8 md:p-12 flex flex-col md:flex-row items-center justify-between overflow-hidden relative group shadow-soft backdrop-blur-lg">
                            <div className="relative z-10 mb-6 md:mb-0 text-center md:text-left">
                                <h3 className="text-3xl md:text-4xl font-display font-bold mb-2">Ready to Transform?</h3>
                                <p className="text-indigo-200">Join 500+ companies using Zedny today.</p>
                            </div>
                            <button
                                onClick={() => navigate('/chat')}
                                className="relative z-10 px-8 py-4 bg-white text-slate-900 font-semibold rounded-2xl hover:scale-105 hover:bg-indigo-50 transition-all shadow-xl"
                            >
                                Get Started
                            </button>

                            <div className="absolute right-0 top-0 h-full w-1/3 bg-gradient-to-l from-indigo-600/20 to-transparent skew-x-12 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-white/5 py-12 bg-[#020617]">
                <div className="container mx-auto px-6 text-center text-gray-500 text-sm">
                    <p>© 2026 Zedny.ai Inc. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
