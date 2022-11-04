<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import { from_ymd, is_today, to_ymd } from "src/date";
    import Meal from "comp/Meal.svelte";
    import NoMeal from "comp/NoMeal.svelte";
    import Week from "comp/Week.svelte";

    function fetch_meal() {
        is_loading = true;
        is_fail = false;
        is_none = false;

        fetch(`/api/meal?edu=${params.edu}&school=${params.school}&date=${to_ymd(params.date)}`)
            .then((resp) => resp.json())
            .then((json) => {
                is_loading = false;

                if (json.code == null) {
                    params.json = json;
                } else {
                    if (json.code == "meal.result_none") {
                        is_none = true;
                    } else {
                        is_fail = true;
                        fail_message = json.message;
                    }
                }
            })
            .catch(() => {
                alert("알 수 없는 오류가 발생했습니다.");
                is_loading = false;
                is_fail = true;
                fail_message = "알 수 없는 오류가 발생했습니다.";
            });
    }

    /** @type {Object} */
    export let params = {};

    $: if (params.date == null) {
        params.date = new Date();
        fetch_meal();
    } else if (typeof params.date == "string") {
        params.date = from_ymd(params.date);
        fetch_meal();
    }

    if (params.date == null) {
        params.date = new Date();
    } else {
        params.date = from_ymd(params.date);

        if (is_today(params.date)) {
            push(`/meal/${params.edu}/${params.school}`);
        }
    }

    let is_loading = true;

    let is_fail = false;
    let fail_message = "";

    let is_none = false;

    onMount(() => {
        fetch_meal();
    });
</script>

<div class="lf">
    <a href="#/">학교 검색하기</a>
</div>

{#if is_loading}
    <div class="message-box l">
        <p>급식 정보를 불러오고 있습니다...</p>
    </div>
{:else if is_fail}
    <div class="message-box l">
        <p>{fail_message}</p>
        <button
            class="button"
            on:click="{() => {
                fetch_meal();
            }}">다시 시도하기</button>
    </div>
{:else if is_none}
    <NoMeal params="{params}" />
{:else}
    <Meal params="{params}" />
{/if}

{#if is_loading == false && is_fail == false}
    <Week params="{params}" />
{/if}

<style>
    .lf {
        padding-bottom: 3px;
        border-bottom: 0.7px solid var(--color);
    }
</style>
