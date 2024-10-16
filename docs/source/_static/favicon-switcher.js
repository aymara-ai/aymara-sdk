(function () {
  function updateFavicon() {
    var link = document.querySelector("link[rel~='icon']");
    if (!link) {
      link = document.createElement("link");
      link.rel = "icon";
      document.getElementsByTagName("head")[0].appendChild(link);
    }

    if (
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches
    ) {
      link.href = "_static/favicon-dark.png";
    } else {
      link.href = "_static/favicon-light.png";
    }
  }

  // Run on initial load
  updateFavicon();

  // Listen for changes
  window.matchMedia("(prefers-color-scheme: dark)").addListener(updateFavicon);
})();
