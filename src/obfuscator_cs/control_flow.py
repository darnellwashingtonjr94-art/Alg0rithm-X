import random
from typing import Dict, List, Tuple

class ControlFlowFlattener:
    """
    Transforms basic linear execution blocks into a non-linear, switch-case state machine dispatcher
    suitable for C# AST obfuscation pipelines.
    """
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def _generate_opaque_predicate(self) -> str:
        """
        Creates mathematical tautologies (always true/false expressions) to confuse static analyzers.
        Example: (x * x + x) % 2 == 0 is always True for integer x.
        """
        var_name = f"op_{random.randint(1000, 9999)}"
        return f"int {var_name} = DateTime.Now.Ticks > 0 ? 1 : 0;"

    def flatten_instructions(self, basic_blocks: List[str]) -> str:
        """
        Transforms a sequential list of C# code statements into a flattened state machine loop.
        """
        block_count = len(basic_blocks)
        indices = list(range(1, block_count + 1))
        
        # Generate non-linear state mapping
        scrambled_indices = indices.copy()
        random.shuffle(scrambled_indices)
        
        state_map: Dict[int, Tuple[str, int]] = {}
        for i in range(block_count):
            curr_state = scrambled_indices[i]
            next_state = scrambled_indices[i + 1] if i + 1 < block_count else 0
            state_map[curr_state] = (basic_blocks[i], next_state)

        initial_state = scrambled_indices[0] if scrambled_indices else 0
        
        # Construct C# control flow code structure
        cs_output = []
        cs_output.append(self._generate_opaque_predicate())
        cs_output.append(f"int state = {initial_state};")
        cs_output.append("while (state != 0)\n{")
        cs_output.append("    switch (state)\n    {")

        for state, (code, next_st) in state_map.items():
            cs_output.append(f"        case {state}:")
            cs_output.append(f"            {code}")
            cs_output.append(f"            state = {next_st};")
            cs_output.append("            break;")

        cs_output.append("        default:")
        cs_output.append("            state = 0;")
        cs_output.append("            break;")
        cs_output.append("    }\n}")

        return "\n".join(cs_output)
