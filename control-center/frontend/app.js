function triggerGoal() {
    const input = document.getElementById('goalInput').value;
    const box = document.getElementById('executionResult');
    if (!input) return;
    box.innerText = "Executing workflow: " + input + "...\n[System] Founder Intelligence, Research Intelligence & Software Factory active.";
}
