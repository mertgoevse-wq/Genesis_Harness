"""Customer intelligence engine for persona, ICP, pain points, and feedback."""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class CustomerPersona:
    name: str
    role: str
    industry: str
    goals: List[str]
    pain_points: List[str]
    objections: List[str]
    buying_signals: List[str]


@dataclass
class IdealCustomerProfile:
    segment: str
    company_size: str
    revenue_range: str
    pain_score: float
    willingness_to_pay: float
    fit_score: float


class CustomerIntelligenceEngine:
    """Generates customer intelligence for a product idea."""

    def analyze(self, idea: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Return full customer intelligence analysis for an idea."""
        personas = self.generate_personas(idea, context)
        icp = self.discover_icp(idea, context)
        pain = self.extract_pain_points(idea, context)
        objections = self.analyze_objections(idea, context)
        signals = self.detect_buying_signals(idea, context)
        return {
            "idea": idea,
            "personas": personas,
            "icp": icp,
            "pain_points": pain,
            "objections": objections,
            "buying_signals": signals,
            "interview_script": self.generate_interview_script(idea, pain),
        }

    def generate_personas(
        self, idea: str, context: Dict[str, Any]
    ) -> List[CustomerPersona]:
        audience = context.get("target_audience", "professionals")
        return [
            CustomerPersona(
                name="Primary User",
                role=f"{audience} operator",
                industry=context.get("industry", "SaaS"),
                goals=[
                    f"Reduce time spent on {idea}",
                    "Improve accuracy and consistency",
                    "Scale operations without proportional hiring",
                ],
                pain_points=[
                    f"Manual {idea} workflows are error-prone",
                    "Lack of real-time visibility",
                    "Integration gaps between tools",
                ],
                objections=[
                    "Concerned about data privacy",
                    "Unsure if ROI justifies cost",
                    "Worried about onboarding complexity",
                ],
                buying_signals=[
                    "Recently hired for growth",
                    "Uses multiple point solutions",
                    "Complained about current process on social media",
                ],
            )
        ]

    def discover_icp(
        self, idea: str, context: Dict[str, Any]
    ) -> IdealCustomerProfile:
        company_size = context.get("company_size", "10-100 employees")
        return IdealCustomerProfile(
            segment=context.get("target_audience", "SMBs"),
            company_size=company_size,
            revenue_range=context.get("revenue_range", "$1M-$10M ARR"),
            pain_score=context.get("pain_score", 75.0),
            willingness_to_pay=context.get("willingness_to_pay", 60.0),
            fit_score=self._fit_score(context),
        )

    def extract_pain_points(self, idea: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        pains = [
            {"pain": f"Manual {idea} is slow", "severity": 9.0, "frequency": "daily"},
            {"pain": "No single source of truth", "severity": 8.0, "frequency": "daily"},
            {"pain": "Reporting is manual and delayed", "severity": 7.0, "frequency": "weekly"},
        ]
        return pains

    def analyze_objections(self, idea: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"objection": "Too expensive", "frequency": "common", "response": "Show ROI within first month"},
            {"objection": "Hard to integrate", "frequency": "common", "response": "Provide native integrations and API"},
            {"objection": "We can build it internally", "frequency": "occasional", "response": "Compare build vs. buy total cost"},
        ]

    def detect_buying_signals(self, idea: str, context: Dict[str, Any]) -> List[str]:
        return [
            f"Searched for {idea} solutions in the last 30 days",
            "Visited pricing page twice in one week",
            "Downloaded a related whitepaper",
            "Started a free trial of a competitor",
        ]

    def generate_interview_script(
        self, idea: str, pain_points: List[Dict[str, Any]]
    ) -> List[str]:
        questions = [
            f"How do you currently handle {idea}?",
            "What is the most frustrating part of that process?",
            "How much time does it take per week?",
            "What tools do you use today?",
            "What would make you switch to a new solution?",
        ]
        for pain in pain_points:
            questions.append(f"How often do you experience: {pain['pain']}?")
        return questions

    def _fit_score(self, context: Dict[str, Any]) -> float:
        pain = context.get("pain_score", 75.0)
        pay = context.get("willingness_to_pay", 60.0)
        budget = context.get("budget_score", 70.0)
        return round((pain + pay + budget) / 3.0, 2)
