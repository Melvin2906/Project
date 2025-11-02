const input = document.getElementById("user-Input");
const suggestionsBox = document.getElementById("suggestions");

input.addEventListener("input", async () => {
    const query = input.value.trim();
    if (!query) {
        suggestionsBox.innerHTML = "";
        return;
    }

    try {
        const res = await fetch(`/suggest?q=${encodeURIComponent(query)}`);
        const data = await res.json();

        // Nettoyer l'affichage
        suggestionsBox.innerHTML = "";

        data.forEach(s => {
            const li = document.createElement("li");
            li.textContent = s;

            li.onclick = () => {
                input.value = s; // Complète l'input
                suggestionsBox.innerHTML = "";
            };

            suggestionsBox.appendChild(li);
        });
    } catch (err) {
        console.error("Erreur fetch suggestions:", err);
    }
});
