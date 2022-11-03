<script>
    import { onMount } from "svelte";
    import { push } from "svelte-spa-router";
    import { from_ymd, is_today, to_ymd } from "src/date";
    import Meal from "comp/Meal.svelte";
    import NoMeal from "comp/NoMeal.svelte";
    import Week from "comp/Week.svelte";

    /** @type {Object} */
    export let params = {};

    if (params.date == null) {
        params.date = new Date();
    } else {
        params.date = from_ymd(params.date);

        if (is_today(params.date)) {
            push(`/move/${params.edu}/${params.school}`);
        }
    }

    let is_loading = true;

    let is_fail = false;
    let fail_message = "";

    let is_none = false;

    onMount(() => {
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
    });
</script>

{#if is_loading}
    <div class="message-box l">
        <p>급식 정보를 불러오고 있습니다...</p>
    </div>
{:else if is_fail}
    <div class="message-box l">
        <p>{fail_message}</p>
        <div class="buttons">
            <a class="button" href="#/">학교 검색하기</a>
            <button
                class="button"
                on:click="{() => {
                    location.reload();
                }}">페이지 새로고침</button>
        </div>
    </div>
{:else if is_none}
    <NoMeal params="{params}" />
{:else}
    <Meal params="{params}" />
{/if}

<Week params="{params}" />
