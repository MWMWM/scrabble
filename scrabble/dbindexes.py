from models import UserProfile
from dbindexer.lookups import StandardLookup
from dbindexer.api import register_index

register_index(UserProfile, {'user__username': StandardLookup(),
})

