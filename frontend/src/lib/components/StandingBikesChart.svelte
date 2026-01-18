<script>
    import { onMount, onDestroy } from "svelte";
    import Chart from "chart.js/auto";

    export let loaded_bike_standing_times = [];

    let canvas, chart;

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

    function isTimeInRange(t, start, end) {
        // same-day range (adjust if you need midnight-crossing)
        return t >= start && t <= end;
    }

    function get_location_count(data, tSec) {
        return data.filter((item) => {
            const startSec = dateStringToSeconds(item.start_time);
            const endSec = dateStringToSeconds(item.end_time);
            return isTimeInRange(tSec, startSec, endSec);
        }).length;
    }

    function secondsToHHMMSS(totalSec) {
        const h = String(Math.floor(totalSec / 3600)).padStart(2, "0");
        const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, "0");
        const s = String(totalSec % 60).padStart(2, "0");
        return `${h}:${m}:${s}`;
    }

    function get_graph_data(data) {
        console.log(data);
        const step = 10;
        const day = 24 * 3600;

        const labels = [];
        const counts = [];

        for (let t = 0; t < day; t += step) {
            labels.push(secondsToHHMMSS(t));
            counts.push(get_location_count(data, t));
        }
        return { labels, counts };
    }

    function render() {
        const { labels, counts } = get_graph_data(loaded_bike_standing_times);
        console.log(loaded_bike_standing_times);

        if (chart) chart.destroy();
        chart = new Chart(canvas, {
            type: "line",
            data: {
                labels,
                datasets: [
                    { label: "Standing bikes", data: counts, pointRadius: 0 },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { maxTicksLimit: 12 } },
                    y: { beginAtZero: true },
                },
            },
        });
    }

    onMount(render);
    $: render(); // rerender when loaded_bike_standing_times changes
    onDestroy(() => chart?.destroy());
</script>

<div style="height:320px">
    <canvas bind:this={canvas}></canvas>
</div>
