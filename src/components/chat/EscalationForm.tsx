import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageSquare, CheckCircle, GraduationCap, Building2 } from 'lucide-react';
import type { EscalationData } from '../../types';

interface Props {
    onSubmit: (data: EscalationData) => void;
    lang?: 'en' | 'ar';
}

const TRANSLATIONS = {
    en: {
        title: 'Support Request',
        fullName: 'Full Name',
        enterName: 'Enter your full name',
        email: 'Email Address',
        enterEmail: 'name@example.com',
        phone: 'Phone Number',
        enterPhone: '+1 234 567 890',
        continue: 'Continue',
        represent: 'I represent...',
        individual: 'Individual / Student',
        company: 'Company / Business',
        institution: 'Institution',
        schoolName: 'School or University Name',
        companyName: 'Company Name',
        enterCompanyName: 'Enter Company Name',
        submit: 'Submit Request',
        goBack: 'Go Back',
        errName: 'Name must be at least 2 characters',
        errEmail: 'Please enter a valid email address',
        errPhone: 'Phone number must be exactly 11 digits'
    },
    ar: {
        title: 'طلب دعم فني',
        fullName: 'الاسم الكامل',
        enterName: 'أدخل اسمك الكامل',
        email: 'البريد الإلكتروني',
        enterEmail: 'name@example.com',
        phone: 'رقم الهاتف',
        enterPhone: '+20 1XX XXX XXXX',
        continue: 'استمرار',
        represent: 'أنا أمثل...',
        individual: 'فرد / طالب',
        company: 'شركة / بيزنس',
        institution: 'المؤسسة التعليمية',
        schoolName: 'اسم المدرسة أو الجامعة',
        companyName: 'اسم الشركة',
        enterCompanyName: 'أدخل اسم الشركة',
        submit: 'إرسال الطلب',
        goBack: 'رجوع',
        errName: 'يجب أن يكون الاسم حرفين على الأقل',
        errEmail: 'يرجى إدخال بريد إلكتروني صحيح',
        errPhone: 'يجب أن يكون رقم الهاتف 11 رقم بالضبط'
    }
};

export const EscalationForm: React.FC<Props> = ({ onSubmit, lang = 'en' }) => {
    const t = TRANSLATIONS[lang];
    const isAr = lang === 'ar';
    const [step, setStep] = useState(1);
    const [errors, setErrors] = useState<{ [key: string]: string }>({});
    const [data, setData] = useState<EscalationData>({
        name: '', email: '', phone: '', userType: null, description: 'AI_GENERATED'
    });

    const isCompany = data.userType === 'company';
    const isStudent = data.userType === 'student';

    const validateStep1 = () => {
        const newErrors: { [key: string]: string } = {};

        if (data.name.trim().length < 2) {
            newErrors.name = t.errName;
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            newErrors.email = t.errEmail;
        }

        // Clean phone of non-digits for length check
        const cleanPhone = data.phone.replace(/\D/g, '');
        if (cleanPhone.length !== 11) {
            newErrors.phone = t.errPhone;
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleNext = () => {
        if (validateStep1()) setStep(prev => prev + 1);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (validateStep1()) onSubmit(data);
    };

    return (
        <div
            dir={isAr ? 'rtl' : 'ltr'}
            className={`w-full bg-slate-900/80 rounded-2xl p-6 border border-indigo-500/30 shadow-2xl backdrop-blur-md relative overflow-hidden group ${isAr ? 'font-arabic' : ''}`}
        >
            {/* Glossy Effect */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-indigo-500" />

            <h3 className={`text-lg font-bold text-white mb-6 flex items-center gap-3 ${isAr ? 'flex-row-reverse' : ''}`}>
                <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400">
                    <MessageSquare className="w-5 h-5" />
                </div>
                {t.title}
            </h3>

            <form onSubmit={handleSubmit} className="space-y-5">
                {step === 1 && (
                    <motion.div initial={{ opacity: 0, x: isAr ? -20 : 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                        <div className="space-y-1">
                            <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.fullName}</label>
                            <input
                                className={`w-full bg-black/20 border rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none transition-all ${errors.name ? 'border-red-500/50' : 'border-indigo-500/20 focus:border-indigo-500/50'}`}
                                placeholder={t.enterName}
                                value={data.name}
                                onChange={e => {
                                    setData({ ...data, name: e.target.value });
                                    if (errors.name) setErrors({ ...errors, name: '' });
                                }}
                                required
                            />
                            {errors.name && <p className="text-[10px] text-red-500 font-medium px-2">{errors.name}</p>}
                        </div>
                        <div className="space-y-1">
                            <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.email}</label>
                            <input
                                className={`w-full bg-black/20 border rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none transition-all ${errors.email ? 'border-red-500/50' : 'border-indigo-500/20 focus:border-indigo-500/50'}`}
                                placeholder={t.enterEmail}
                                type="email"
                                value={data.email}
                                onChange={e => {
                                    setData({ ...data, email: e.target.value });
                                    if (errors.email) setErrors({ ...errors, email: '' });
                                }}
                                required
                            />
                            {errors.email && <p className="text-[10px] text-red-500 font-medium px-2">{errors.email}</p>}
                        </div>
                        <div className="space-y-1">
                            <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.phone}</label>
                            <input
                                className={`w-full bg-black/20 border rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none transition-all ${errors.phone ? 'border-red-500/50' : 'border-indigo-500/20 focus:border-indigo-500/50'}`}
                                placeholder={t.enterPhone}
                                value={data.phone}
                                onChange={e => {
                                    setData({ ...data, phone: e.target.value });
                                    if (errors.phone) setErrors({ ...errors, phone: '' });
                                }}
                                required
                            />
                            {errors.phone && <p className="text-[10px] text-red-500 font-medium px-2">{errors.phone}</p>}
                        </div>
                        <button type="button" onClick={handleNext} className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 rounded-xl mt-2 transition-all shadow-lg shadow-indigo-600/20 active:scale-[0.98]">
                            {t.continue}
                        </button>
                    </motion.div>
                )}

                {step === 2 && (
                    <motion.div initial={{ opacity: 0, x: isAr ? -20 : 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
                        <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.represent}</label>
                        <div className="grid grid-cols-2 gap-4">
                            <button
                                type="button"
                                onClick={() => setData({ ...data, userType: 'student' })}
                                className={`p-4 rounded-2xl border flex flex-col items-center gap-3 transition-all duration-300 ${isStudent ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-glow' : 'bg-black/20 border-white/5 hover:bg-white/5 text-gray-400'}`}
                            >
                                <GraduationCap className={`w-8 h-8 ${isStudent ? 'text-indigo-400' : 'text-slate-500'}`} />
                                <span className="text-xs font-bold">{t.individual}</span>
                            </button>
                            <button
                                type="button"
                                onClick={() => setData({ ...data, userType: 'company' })}
                                className={`p-4 rounded-2xl border flex flex-col items-center gap-3 transition-all duration-300 ${isCompany ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-glow' : 'bg-black/20 border-white/5 hover:bg-white/5 text-gray-400'}`}
                            >
                                <Building2 className={`w-8 h-8 ${isCompany ? 'text-indigo-400' : 'text-slate-500'}`} />
                                <span className="text-xs font-bold">{t.company}</span>
                            </button>
                        </div>

                        {data.userType && (
                            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="space-y-4 pt-2">
                                {isStudent ? (
                                    <div className="space-y-1">
                                        <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.institution}</label>
                                        <input
                                            placeholder={t.schoolName}
                                            value={data.institution || ''}
                                            onChange={e => setData({ ...data, institution: e.target.value })}
                                            className="w-full bg-black/20 border border-indigo-500/20 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-indigo-500/50"
                                            required
                                        />
                                    </div>
                                ) : (
                                    <div className="space-y-1">
                                        <label className={`text-[10px] text-indigo-300 font-bold uppercase tracking-widest ${isAr ? 'pr-1 block' : 'pl-1'}`}>{t.companyName}</label>
                                        <input
                                            placeholder={t.enterCompanyName}
                                            value={data.companyName || ''}
                                            onChange={e => setData({ ...data, companyName: e.target.value })}
                                            className="w-full bg-black/20 border border-indigo-500/20 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-indigo-500/50"
                                            required
                                        />
                                    </div>
                                )}
                                <button type="submit" className={`w-full bg-green-600 hover:bg-green-500 text-white font-bold py-3.5 rounded-xl mt-4 transition-all shadow-lg shadow-green-600/20 active:scale-[0.98] flex items-center justify-center gap-2 ${isAr ? 'flex-row-reverse' : ''}`}>
                                    <CheckCircle className="w-5 h-5" />
                                    {t.submit}
                                </button>
                            </motion.div>
                        )}

                        <button type="button" onClick={() => setStep(1)} className="w-full text-xs text-slate-500 hover:text-slate-300 font-medium py-2 transition-colors">
                            {t.goBack}
                        </button>
                    </motion.div>
                )}
            </form>
        </div>
    );
};
