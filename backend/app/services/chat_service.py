import os
from typing import List, Optional
from app.models.car import Car
import json

# Mock AI service - replace with actual OpenAI integration
class ChatService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
    
    def answer_question(
        self,
        question: str,
        current_cars: List[Car],
        current_car: Optional[Car] = None,
        saved_cars: Optional[List[Car]] = None,
    ) -> str:
        """
        Answer a user question about cars using mock AI.
        In production, this would call OpenAI API.
        """
        
        if saved_cars is None:
            saved_cars = []
        
        # Build context
        context = self._build_context(current_cars, current_car, saved_cars)
        
        # Mock response based on question patterns
        response = self._generate_mock_response(question, context)
        
        return response
    
    def _build_context(
        self,
        current_cars: List[Car],
        current_car: Optional[Car],
        saved_cars: List[Car],
    ) -> str:
        """Build context string from car data"""
        context_parts = []
        
        if current_car:
            context_parts.append(f"Current car: {current_car.make} {current_car.model} ({current_car.year}), ${current_car.price}, {current_car.mileage} miles")
        
        if current_cars:
            context_parts.append(f"Search results: {len(current_cars)} cars")
            for car in current_cars[:5]:  # Limit to first 5
                context_parts.append(f"  - {car.make} {car.model} ({car.year}): ${car.price}")
        
        if saved_cars:
            context_parts.append(f"Saved cars: {len(saved_cars)}")
            for car in saved_cars[:5]:
                context_parts.append(f"  - {car.make} {car.model} ({car.year}): ${car.price}")
        
        return "\n".join(context_parts)
    
    def _generate_mock_response(self, question: str, context: str) -> str:
        """Generate a mock response - replace with actual AI"""
        question_lower = question.lower()
        
        # Simple pattern matching for demo
        if "expensive" in question_lower or "most expensive" in question_lower:
            return "Looking at the search results, the most expensive car is priced at $45,000. It's a Tesla Model 3 from 2023 with low mileage."
        elif "cheap" in question_lower or "cheapest" in question_lower or "least expensive" in question_lower:
            return "The most affordable option in the results is $24,000 - a Honda Civic from 2021 with about 22,000 miles."
        elif "save" in question_lower or "saved" in question_lower:
            return "You have saved cars in your collection. Would you like me to compare them or show you more details?"
        elif "mileage" in question_lower:
            return "Mileage is an important factor. Lower mileage generally means the car has been driven less and may have more longevity."
        elif "recommend" in question_lower or "suggestion" in question_lower:
            return "Based on the current search, I'd recommend checking out the cars with the best mileage-to-price ratio. Would you like me to help you compare specific models?"
        else:
            return f"I can help you with questions about the cars we're viewing. You asked: {question}\n\nContext: {context[:200]}... \n\nFor more specific information, please refine your question."


chat_service = ChatService()
