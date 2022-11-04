<script>
    import { onMount } from "svelte";
    export let params = {};

    onMount(() => {
        document.title = "급식 정보 없음";
    });
</script>

<div class="message-box l">
    <span class="date">
        {params.date.toLocaleDateString()}
    </span>
    <p><span class="high">급식</span> 정보가 없습니다.</p>
</div>

<style>
    span.date {
        padding-bottom: 3px;
        border-bottom: 0.7px solid #bcbcbc;
    }
</style>
