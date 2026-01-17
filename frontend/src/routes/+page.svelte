<script lang="ts">
    import { onMount } from "svelte";

    const API_BASE = "http://127.0.0.1:4001";

    onMount(async () => {
        cities = fetch(`${API_BASE}/api/cities`).then((res) => res.json());
        await import("cally");
    });

    let selected_date = $state("");
    let selected_city = $state("");
    let selected_step_size = $state("1min");
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
</script>

<fieldset
    class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4"
>
    <legend class="fieldset-legend">Controls</legend>
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
    <label for="stepsize-chooser" class="label">Choose stepsize</label>
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
    Heatmap
    Places in Heatmap markieren
    In einem Graphen anzeigen wie viele Fahrräder gerade ausgeliehen sind (+ anzeige wo man da gerade ist von der Uhrzeit her)
    Slider für die Zeit
-->
