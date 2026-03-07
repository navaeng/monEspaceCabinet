from data.database import supabase_client


def get_post_instruction(uid):
    select_instruction_post = (
        supabase_client.table("posts")
        .select("instruction_post")
        .eq("user_id", uid)
        .limit(1)
    ).execute()
    post_data = get_post_instruction.data
    if (
        post_data
        and isinstance(post_data, list)
        and len(post_data) > 0
    ):
        first_item = post_data[0]
        if isinstance(first_item, dict):
            post = str(first_item.get("instruction_post") or "")
    return select_instruction_post