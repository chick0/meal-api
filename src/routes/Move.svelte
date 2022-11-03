<script>
    import { replace } from "svelte-spa-router";
    export let params = {};

    replace(`/meal/${params.edu}/${params.school}/${params.date == null ? "" : params.date}`);
</script>
