from osmchangesets.osm.api import API
from datetime import timedelta

api = API()

# ==============================================================================
# get the latest changesets and print unique users
# ==============================================================================
changesets = api.latest_changesets()
users = set()
for changeset in changesets:
    users.add(changeset.user)
print(f"Unique users: {", ".join(users)} for the last {len(changesets)} changesets")
# find out what the largest bounding box is by looking at the area for each changeset's bounds
largest_area = 0
largest_changeset = None
for changeset in changesets:
    if changeset.bounds.area > largest_area:
        largest_area = changeset.bounds.area
        largest_changeset = changeset
print(
    f"The largest changeset is {largest_changeset.osm_id} with a bounding box area of {largest_area}"  # type: ignore
)

# ==============================================================================
# get a specific changeset
# ==============================================================================
changeset = api.get_changeset(7053134)
if changeset:
    print(
        f"Changeset {changeset.osm_id} by {changeset.user} has {changeset.changes_count} changes"
    )

# ==============================================================================
# get changesets 1, 2, 3
# ==============================================================================
changesets = api.get_changesets([1, 2, 3])
for changeset in changesets:
    print(
        f"Changeset {changeset.osm_id} by {changeset.user} has {changeset.changes_count} changes"
    )

# ==============================================================================
# query changesets, user mvexel in Netherlands
# ==============================================================================
changesets = api.query_changesets(display_name="mvexel", bbox=(3.2, 50.8, 7.2, 53.6))
print(
    f"user mvexel has {len(changesets)} changesets in the Netherlands, the oldest is from {changesets[-1].created_at} and the newest is from {changesets[0].created_at}"
)
