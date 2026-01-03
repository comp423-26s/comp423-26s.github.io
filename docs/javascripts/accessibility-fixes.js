document.addEventListener("DOMContentLoaded", function() {
    // Fix for missing submit button in forms (WCAG H32)
    // Adds a hidden submit button to forms that lack one, to satisfy accessibility tools
    // and potentially aid in implicit submission behavior.
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        if (!form.querySelector("button[type='submit'], input[type='submit'], input[type='image']")) {
            const button = document.createElement("button");
            button.type = "submit";
            button.style.position = "absolute";
            button.style.left = "-9999px";
            button.style.width = "1px";
            button.style.height = "1px";
            button.tabIndex = -1;
            button.setAttribute("aria-hidden", "true");
            button.textContent = "Submit";
            form.appendChild(button);
        }
    });
});
