<script lang="ts">
    import "../../app.css";
    import Header from "$lib/components/ui/header/header.svelte";
    const apiKey = import.meta.env.VITE_API_URL;
</script>

<div
    class="h-full bg-rich_black text-white padding: 0 !important"
    style="font-family: 'Open Sans';"
>
    <Header showGradient={false}></Header>
    <slot></slot>
</div>

<style>
    @import url("https://fonts.googleapis.com/css2?family=Open+Sans:wght@200;300;400;600;700&display=swap");
</style>
