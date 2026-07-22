const generateBtn = document.getElementById("generateBtn");
const statusEl = document.getElementById("status");
const results = document.getElementById("results");
const lessonList = document.getElementById("lessonList");
const quizContainer = document.getElementById("quizContainer");

generateBtn.addEventListener("click", async () => {
  const topic = document.getElementById("topic").value.trim();
  const grade = document.getElementById("grade").value;

  if (!topic) {
    statusEl.textContent = "Please enter a topic first.";
    return;
  }

  statusEl.textContent = "Generating lesson + quiz...";
  results.classList.add("hidden");
  generateBtn.disabled = true;

  try {
    const res = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, grade }),
    });
    const data = await res.json();

    if (!res.ok) {
      statusEl.textContent = data.error || "Something went wrong.";
      return;
    }

    statusEl.textContent = "";
    renderLesson(data.lesson_summary);
    renderQuiz(data.quiz);
    results.classList.remove("hidden");
  } catch (err) {
    statusEl.textContent = "Network error: " + err.message;
  } finally {
    generateBtn.disabled = false;
  }
});

function renderLesson(points) {
  lessonList.innerHTML = "";
  points.forEach((p) => {
    const li = document.createElement("li");
    li.textContent = p;
    lessonList.appendChild(li);
  });
}

function renderQuiz(questions) {
  quizContainer.innerHTML = "";
  questions.forEach((q, qIndex) => {
    const qDiv = document.createElement("div");
    qDiv.className = "quiz-question";

    const qText = document.createElement("p");
    qText.className = "q-text";
    qText.textContent = `${qIndex + 1}. ${q.question}`;
    qDiv.appendChild(qText);

    const explanation = document.createElement("div");
    explanation.className = "explanation";
    explanation.textContent = q.explanation || "";

    q.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className = "option-btn";
      btn.textContent = opt;
      const optionLetter = opt.trim().charAt(0);

      btn.addEventListener("click", () => {
        const buttons = qDiv.querySelectorAll(".option-btn");
        buttons.forEach((b) => (b.disabled = true));

        if (optionLetter === q.correct_answer) {
          btn.classList.add("correct");
        } else {
          btn.classList.add("incorrect");
          buttons.forEach((b) => {
            if (b.textContent.trim().charAt(0) === q.correct_answer) {
              b.classList.add("correct");
            }
          });
        }
        explanation.style.display = "block";
      });

      qDiv.appendChild(btn);
    });

    qDiv.appendChild(explanation);
    quizContainer.appendChild(qDiv);
  });
}
