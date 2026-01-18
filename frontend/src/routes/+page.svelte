<script lang="ts">
    import Heatmap from "$lib/components/Heatmap.svelte";
    import StandingBikesChart from "$lib/components/StandingBikesChart.svelte";
    import { onMount } from "svelte";

    const API_BASE = "http://127.0.0.1:4001";

    onMount(async () => {
        cities = fetch(`${API_BASE}/api/cities`).then((res) => res.json());
        await import("cally");
    });

    let selected_date = $state("2025-11-01");
    let selected_city = $state("1");
    let selected_step_size = $state("1min");
    let selected_time = $state(720);
    let step_size_in_s = $derived.by(() => {
        switch (selected_step_size) {
            case "10s":
                return 10;
            case "1min":
                return 60;
            case "10min":
                return 600;
            case "1h":
                return 3600;
            default:
                return 60; // Default to 1 minute if nothing is selected
        }
    });
    let cities:
        | Promise<
              {
                  country_id: number;
                  uid: string;
                  name: string;
                  alias: string;
                  lat: number;
                  lng: number;
                  lat_min: number;
                  lng_min: number;
                  lat_max: number;
                  lng_max: number;
              }[]
          >
        | undefined = $state();

    let bike_standing_times = $derived.by(() => {
        if (!selected_city || selected_city === "") return [];
        if (!selected_date || selected_date === "") return [];

        const start = `${selected_date} 00:00:00`;
        const end = `${selected_date} 23:59:59`;

        return fetch(
            `${API_BASE}/api/active_standing_times/${selected_city}` +
                `?timestamp_start=${start}&timestamp_end=${end}`,
        ).then((res) => res.json());
    });
    let bike_trips = $derived.by(() => {});

    function timeToSeconds(h, m, s) {
        return h * 3600 + m * 60 + s;
    }

    function dateStringToSeconds(dateStr) {
        const d = new Date(dateStr); // GMT handled automatically
        return timeToSeconds(
            d.getUTCHours(),
            d.getUTCMinutes(),
            d.getUTCSeconds(),
        );
    }

    function isTimeInRange(targetSec, startSec, endSec) {
        // normal range (same day)
        if (startSec <= endSec) {
            return targetSec >= startSec && targetSec <= endSec;
        }
        // crosses midnight
        return targetSec >= startSec || targetSec <= endSec;
    }

    function get_locations(loaded_bike_standing_times, hhmmss) {
        return loaded_bike_standing_times
            .filter((item) => {
                const startSec = dateStringToSeconds(item.start_time);
                const endSec = dateStringToSeconds(item.end_time);
                return isTimeInRange(hhmmss, startSec, endSec);
            })
            .map((item) => [item.latitude, item.longitude]);
    }

    function get_graph_data(loaded_bike_standing_times) {
        const step = 10; // 10-second intervals
        const daySeconds = 24 * 60 * 60;

        const series = [];
        for (let t = 0; t < daySeconds; t += step) {
            const locations = get_locations(loaded_bike_standing_times, t);
            series.push({ t, count: locations.length });
        }
        return series;
    }

    function formatTime(totalSeconds: number): string {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = parseInt((totalSeconds % 3600) / 60);
        return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}`;
    }
</script>

<fieldset
    class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4 m-2 shadow-2xl"
>
    <!-- Choose city -->
    <label for="city-chooser" class="label">City</label>
    <select id="city-chooser" class="select" bind:value={selected_city}>
        {#await cities}
            <option disabled selected>Cities are loading...</option>
        {:then loaded_cities}
            <option disabled selected>Pick a city</option>
            {#each loaded_cities as city}
                <option value={city.uid}>{city.name}</option>
            {/each}
        {:catch error}
            <option disabled selected>{error.message}</option>
        {/await}
    </select>

    <!-- Choose date -->
    <label for="date-chooser" class="label">Date</label>
    <button
        popovertarget="date-chooser-popover"
        class="input input-border"
        id="date-chooser"
        style="anchor-name:--date-chooser"
    >
        {selected_date || "Pick a date"}
    </button>
    <div
        popover
        id="date-chooser-popover"
        class="dropdown bg-base-100 rounded-box shadow-lg"
        style="position-anchor:--date-chooser"
    >
        <!-- svelte-ignore event_directive_deprecated -->
        <calendar-date
            class="cally"
            on:change={(evt: Event) => {
                selected_date = evt.target.value;
            }}
        >
            <calendar-month></calendar-month>
        </calendar-date>
    </div>

    <!-- Choose a step size -->
    <label for="stepsize-chooser" class="label">Stepsize</label>
    <div class="join w-full">
        {#each ["10s", "1min", "10min", "1h"] as step}
            <input
                class="join-item btn flex-1"
                type="radio"
                name="step"
                aria-label={step}
                value={step}
                bind:group={selected_step_size}
            />
        {/each}
    </div>
</fieldset>

<!-- Visualisations:
    Places in Heatmap markieren
    In einem Graphen anzeigen wie viele Fahrräder gerade ausgeliehen sind (+ anzeige wo man da gerade ist von der Uhrzeit her)
    Slider soll stepsize respecten und styling ist komisch
-->

<!-- Time, fixed at the top right -->
<div class="fixed top-2 right-4 hover-3d group">
    <!-- content -->
    <figure class="max-w-100 rounded-2xl">
        <div
            class="transition-all text-center font-mono text-5xl group-hover:text-9xl font-bold text-primary bg-black rounded-box p-1.5"
        >
            {formatTime(selected_time)}
        </div>
    </figure>
    <!-- 8 empty divs needed for the 3D effect -->
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
    <div></div>
</div>

<div
    class="fixed bottom-0 w-screen bg-base-200 border-base-300 border shadow-2xl"
>
    <div class="absolute top-0 -translate-y-full right-0">
        {#await bike_standing_times}
            Loading Bike Standing Times...
        {:then loaded_bike_standing_times}
            <!-- <StandingBikesChart {loaded_bike_standing_times} /> -->
            Graph to slow and buggy currently
        {:catch error}
            {error.message}
        {/await}
    </div>
    <div class="">
        <input
            type="range"
            min="0"
            max="86400"
            step={step_size_in_s}
            bind:value={selected_time}
            class="range range-primary range-xs w-full"
        />

        <div
            class="flex justify-between px-2 mt-2 text-xs text-base-content/50"
        >
            <span>|</span>
            <span>|</span>
            <span>|</span>
            <span>|</span>
            <span>|</span>
        </div>

        <div class="flex justify-between px-2 mt-1 text-xs font-mono">
            <span>00:00</span>
            <span>06:00</span>
            <span>12:00</span>
            <span>18:00</span>
            <span>23:59</span>
        </div>
    </div>
</div>

{#await bike_standing_times}
    Loading Bike Standing Times...
{:then loaded_bike_standing_times}
    <!-- {get_locations(loaded_bike_standing_times, "12:00:00")} -->
    <Heatmap
        bike_positions={get_locations(
            loaded_bike_standing_times,
            selected_time,
        )}
        style="position: absolute; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1"
    ></Heatmap>
{:catch error}
    {error.message}
{/await}
