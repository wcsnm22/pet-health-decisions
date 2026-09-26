// ILANG
// TYPE:worker ROLE:canonical-host-and-real-404
const CANONICAL_HOST = "pet-health-decisions.pages.dev";
const VALID_PATHS = new Set(["/", "/1800petmeds-online-pharmacy", "/about", "/assets/embark-discount-channels.svg", "/assets/embark-kit-results.svg", "/assets/favicon.svg", "/assets/joint-label-compare.svg", "/assets/online-vet-vs-inperson.svg", "/assets/rx-order-flow.svg", "/assets/style.css", "/assets/vetster-plan-compare.svg", "/best-joint-supplement-for-dogs", "/buy-pet-prescription-meds-online", "/contact", "/cosequin-joint-supplement", "/embark-discount-code", "/embark-dna-test", "/embark-dna-test-review", "/online-vet-vs-in-person", "/privacy", "/robots.txt", "/sitemap.xml", "/vetster-online-vet", "/vetster-review"]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.hostname !== CANONICAL_HOST) {
      return Response.redirect(new URL(url.pathname + url.search, `https://${CANONICAL_HOST}`).toString(), 301);
    }

    const path = url.pathname.replace(/\/+$/, "") || "/";

    if (path.endsWith(".html")) {
      const bare = path === "/index.html" ? "/" : path.slice(0, -5);
      if (VALID_PATHS.has(bare)) {
        return Response.redirect(new URL(bare + url.search, `https://${CANONICAL_HOST}`).toString(), 308);
      }
    }

    if (VALID_PATHS.has(path)) {
      return env.ASSETS.fetch(request);
    }

    const notFound = await env.ASSETS.fetch(new URL("/404.html", url));
    return new Response(notFound.body, {
      status: 404,
      headers: {
        "content-type": "text/html; charset=utf-8",
        "cache-control": "no-store",
        "x-robots-tag": "noindex",
      },
    });
  },
};
