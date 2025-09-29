
[...document.querySelectorAll(".md\\:w-1\\/3, div.relative:nth-child(1), .px-8, div.mb-4, div.fixed:nth-child(3)")].forEach(e=>e.style.setProperty('display', 'none'));
document.querySelector(".md\\:flex-1")?.style.setProperty('min-height', '100vh');


(function () {
  if (window.hasPasteScript) return;
  window.hasPasteScript = true;
  // Create styles for the paste button
  const style = document.createElement("style");
  style.textContent = `
        .paste-button-wrapper {
            position: relative;
            display: inline-block;
            width: 100%;
        }
        
        .paste-button {
            position: absolute;
            right: 5px;
            top: 50%;
            transform: translateY(-50%);
            padding: 4px 8px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            z-index: 10;
            transition: background 0.2s;
        }
        
        .paste-button:hover {
            background: #45a049;
        }
        
        .paste-button:active {
            background: #3d8b40;
        }
        
        input.has-paste-button {
            padding-right: 60px !important;
        }
        
        /* For inputs that can't be wrapped */
        .paste-button-absolute {
            position: fixed;
            z-index: 10000;
        }
    `;
  document.head.appendChild(style);

  // Function to trigger input events properly for React/Vue/Angular
  function setNativeValue(element, value) {
    const valueSetter = Object.getOwnPropertyDescriptor(element, "value")?.set;
    const prototype = Object.getPrototypeOf(element);
    const prototypeValueSetter = Object.getOwnPropertyDescriptor(
      prototype,
      "value"
    )?.set;

    if (valueSetter && valueSetter !== prototypeValueSetter) {
      prototypeValueSetter?.call(element, value);
    } else {
      valueSetter?.call(element, value);
    }
  }

  // Function to add paste button to an input
  function addPasteButton(input) {
    // Skip if already has a paste button
    if (input.dataset.hasPasteButton) return;

    input.dataset.hasPasteButton = "true";

    // Create paste button
    const pasteBtn = document.createElement("button");
    pasteBtn.textContent = "Paste";
    pasteBtn.className = "paste-button";
    pasteBtn.type = "button";

    // Handle paste
    pasteBtn.addEventListener("click", async () => {
      try {
        const text = await navigator.clipboard.readText();

        // Focus the input first
        input.focus();

        // Set value using native setter to trigger React
        setNativeValue(input, text);

        // Trigger all possible events
        input.dispatchEvent(
          new Event("input", { bubbles: true, cancelable: true })
        );
        input.dispatchEvent(
          new Event("change", { bubbles: true, cancelable: true })
        );

        // For React 16+
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype,
          "value"
        ).set;
        nativeInputValueSetter.call(input, text);

        // Trigger React's onChange
        const ev1 = new Event("input", { bubbles: true });
        input.dispatchEvent(ev1);

        // Also trigger keyboard events as some forms listen to these
        const ev2 = new KeyboardEvent("keydown", {
          bubbles: true,
          cancelable: true,
          keyCode: 13,
        });
        input.dispatchEvent(ev2);
        const ev3 = new KeyboardEvent("keyup", {
          bubbles: true,
          cancelable: true,
          keyCode: 13,
        });
        input.dispatchEvent(ev3);

        // Blur and refocus to ensure state updates
        input.blur();
        input.focus();

        // Visual feedback
        pasteBtn.textContent = "✓";
        setTimeout(() => {
          pasteBtn.textContent = "Paste";
        }, 1000);
      } catch (err) {
        console.error("Failed to read clipboard:", err);
        pasteBtn.textContent = "✗";
        setTimeout(() => {
          pasteBtn.textContent = "Paste";
        }, 1000);
      }
    });

    // Try to wrap the input
    const parent = input.parentNode;
    const computedStyle = window.getComputedStyle(input);

    // Check if we can wrap the input
    if (parent && !["absolute", "fixed"].includes(computedStyle.position)) {
      try {
        const wrapper = document.createElement("div");
        wrapper.className = "paste-button-wrapper";

        // Copy display style from input
        if (computedStyle.display === "block") {
          wrapper.style.display = "block";
        }

        parent.insertBefore(wrapper, input);
        wrapper.appendChild(input);
        wrapper.appendChild(pasteBtn);

        input.classList.add("has-paste-button");
      } catch (e) {
        // If wrapping fails, use absolute positioning
        useAbsolutePositioning();
      }
    } else {
      // Use absolute positioning as fallback
      useAbsolutePositioning();
    }

    function useAbsolutePositioning() {
      pasteBtn.classList.add("paste-button-absolute");
      document.body.appendChild(pasteBtn);

      function updatePosition() {
        const rect = input.getBoundingClientRect();
        pasteBtn.style.left = rect.right - pasteBtn.offsetWidth - 5 + "px";
        pasteBtn.style.top =
          rect.top + rect.height / 2 - pasteBtn.offsetHeight / 2 + "px";
      }

      updatePosition();

      // Update position on scroll/resize
      let ticking = false;
      function requestUpdate() {
        if (!ticking) {
          requestAnimationFrame(updatePosition);
          ticking = true;
          setTimeout(() => {
            ticking = false;
          }, 100);
        }
      }

      window.addEventListener("scroll", requestUpdate, true);
      window.addEventListener("resize", requestUpdate);

      // Hide button when input is not visible
      const observer = new IntersectionObserver((entries) => {
        pasteBtn.style.display = entries[0].isIntersecting ? "block" : "none";
      });
      observer.observe(input);
    }
  }

  // Process all existing inputs
  function processAllInputs() {
    const inputs = document.querySelectorAll(
      'input[type="text"], input[type="email"], input[type="password"], input[type="search"], input[type="tel"], input[type="url"], input[type="number"], input:not([type])'
    );
    inputs.forEach(addPasteButton);
  }

  // Initial processing
  processAllInputs();

  // Watch for new inputs
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === 1) {
          // Element node
          if (node.matches && node.matches("input")) {
            addPasteButton(node);
          }
          // Check descendants
          const inputs = node.querySelectorAll
            ? node.querySelectorAll("input")
            : [];
          inputs.forEach(addPasteButton);
        }
      });
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
  });
})();




