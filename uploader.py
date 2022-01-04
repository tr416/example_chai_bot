from bot import Replica

from chai_py.auth import set_auth
from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment, share_bot
from chai_py.deployment import advertise_deployed_bot

DEVELOPER_UID = "<DEV_UID_HERE>"
DEVELOPER_KEY = "<DEV_KEY_HERE>"

set_auth(DEVELOPER_UID, DEVELOPER_KEY)

image_url = ""

package(
    Metadata(
        name="<BOT NAME HERE>",
        image_url=image_url,
        color="f1a2b3",
        developer_uid=DEVELOPER_UID,
        description="<BOT DESCRIPTION HERE>",
        input_class=Replica,
    ),
    requirements=["retry", "npu"],
)


bot_uid = upload_and_deploy("_package.zip")
wait_for_deployment(bot_uid)
share_bot(bot_uid)
