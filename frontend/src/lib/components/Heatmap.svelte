<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    // WICHTIG: Type-Only Import! Das crasht den Server nicht.
    import type { Map } from "leaflet";

    let mapElement: HTMLDivElement;
    let mapInstance: Map | undefined;

    onMount(async () => {
        const L = (await import("leaflet")).default;
        await import("leaflet/dist/leaflet.css");
        await import("leaflet.heat");

        if (mapElement) {
            mapInstance = L.map(mapElement).setView([51.505, -0.09], 13);

            L.tileLayer(
                "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
                {
                    attribution:
                        '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: "abcd",
                    maxZoom: 19,
                },
            ).addTo(mapInstance);

            const heat = (L as any)
                .heatLayer(
                    [
                        [51.5, -0.09, 1],
                        [51.51, -0.1, 0.8],
                    ], // Deine Daten
                    { radius: 25 },
                )
                .addTo(mapInstance);
        }
    });

    onDestroy(() => {
        if (mapInstance) {
            mapInstance.remove();
        }
    });
</script>

<div bind:this={mapElement} style="height: 500px; width: 100%;"></div>
