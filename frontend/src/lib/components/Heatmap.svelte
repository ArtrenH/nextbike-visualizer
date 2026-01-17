<script lang="ts">
    import { onMount, onDestroy } from "svelte";
    import type { Map } from "leaflet";

    let mapElement: HTMLDivElement;
    let mapInstance: Map | undefined;

    let heatLayer = $state<any>(undefined);

    let { bike_positions } = $props();

    onMount(async () => {
        const L = (await import("leaflet")).default;
        await import("leaflet/dist/leaflet.css");
        await import("leaflet.heat");

        if (mapElement) {
            mapInstance = L.map(mapElement).setView([51.3399, 12.3735], 13);

            L.tileLayer(
                "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                {
                    attribution:
                        '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: "abcd",
                    maxZoom: 19,
                },
            ).addTo(mapInstance);

            heatLayer = (L as any)
                .heatLayer([], { radius: 10 })
                .addTo(mapInstance);
        }
    });

    $effect(() => {
        if (heatLayer && bike_positions) {
            const formattedData = bike_positions.map((point) => [...point, 40]);
            heatLayer.setLatLngs(formattedData);
        }
    });

    onDestroy(() => {
        if (mapInstance) {
            mapInstance.remove();
        }
    });
</script>

<div bind:this={mapElement} style="height: 500px; width: 100%;"></div>
