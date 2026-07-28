from enum import Enum
from typing import Dict, Any

class ProductState(Enum):
    IDEA = "IDEA"
    RESEARCHING = "RESEARCHING"
    VALIDATING = "VALIDATING"
    DESIGNING = "DESIGNING"
    BUILDING = "BUILDING"
    TESTING = "TESTING"
    DEPLOYING = "DEPLOYING"
    LAUNCHED = "LAUNCHED"
    LEARNING = "LEARNING"

class ProductLifecycleEngine:
    def __init__(self, product_name: str):
        self.product_name = product_name
        self.state = ProductState.IDEA

    def transition_to(self, new_state: ProductState) -> Dict[str, Any]:
        self.state = new_state
        return {"product": self.product_name, "state": self.state.value}
