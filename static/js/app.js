const form = document.getElementById("passenger-form");
const button = document.getElementById("submit-button");
const errorBox = document.getElementById("error-message");
const overlay = document.getElementById("result-overlay");
const resultCard = document.getElementById("result-card");
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.style.display = "none";
  button.disabled = true;
  button.querySelector("span").textContent = "Consulting the manifest...";

  const values = Object.fromEntries(new FormData(form).entries());
  try {
    const response = await fetch("/predict/", {
      method: "POST",
      headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
      body: JSON.stringify(values)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");
    showResult(data);
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.style.display = "block";
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Discover your fate";
  }
});

function showResult(data) {
  const survived = data.survived;
  overlay.hidden = false;
  overlay.classList.toggle("lost", !survived);
  resultCard.className = `result-card ${survived ? "survived" : "lost"}`;
  document.getElementById("result-symbol").textContent = survived ? "⚓ ✦" : "🌊";
  document.getElementById("result-eyebrow").textContent = survived ? "A SAFE ARRIVAL" : "LOST TO THE ATLANTIC";
  document.getElementById("result-title").textContent = survived ? "You survived." : "The voyage ends.";
  document.getElementById("result-message").textContent = data.message;

  const scoreWrap = document.getElementById("score-wrap");
  if (data.score !== null && data.score !== undefined) {
    scoreWrap.hidden = false;
    document.getElementById("score").textContent = `${data.score}%`;
  } else {
    scoreWrap.hidden = true;
  }
  document.getElementById("confetti").replaceChildren();
  if (survived) createCelebration();
}

function createCelebration() {
  const container = document.getElementById("confetti");
  for (let i = 0; i < 65; i++) {
    const piece = document.createElement("i");
    piece.className = "particle";
    piece.style.left = `${Math.random() * 100}%`;
    piece.style.animationDelay = `${Math.random() * 1.6}s`;
    piece.style.animationDuration = `${2.5 + Math.random() * 2}s`;
    piece.style.opacity = `${0.45 + Math.random() * 0.55}`;
    container.appendChild(piece);
  }
}

document.getElementById("again-button").addEventListener("click", () => {
  overlay.hidden = true;
  overlay.classList.remove("lost");
  form.reset();
  window.scrollTo({top: 0, behavior: "smooth"});
});
