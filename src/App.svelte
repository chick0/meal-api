<script>
    import { onMount } from "svelte";
    import Router from "svelte-spa-router";
    import { routes } from "src/router.js";

    /** @type {boolean} */
    let is_component_loading = false;

    onMount(() => {
        window.onunhandledrejection = () => {
            alert("치명적인 오류가 발생해 재시작합니다.");
            window.location.reload();
        };
    });
</script>

<Router
    routes="{routes}"
    on:routeLoading="{() => {
        is_component_loading = true;
    }}"
    on:routeLoaded="{() => {
        is_component_loading = false;
    }}" />
