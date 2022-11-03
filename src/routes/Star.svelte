<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import { get_star } from "src/star";

    let star = get_star();

    onMount(() => {
        document.title = "🌟 즐겨찾기";

        if (star.length == 0) {
            alert("등록된 즐겨찾기가 없습니다!");
            push("/");
        } else if (star.length == 1) {
            push(star[0].path);
        }
    });
</script>

<div class="lf">
    <h1>🌟 즐겨찾기</h1>
    <ol class="list l">
        {#each star as school}
            <li>
                <a href="#{school.path}">{school.name}</a>
            </li>
        {/each}
    </ol>
</div>

<div class="menu">
    <a class="button" href="/#">학교 검색하러 가기</a>
</div>
