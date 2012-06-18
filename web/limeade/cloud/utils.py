from .models import Node


def get_best_node(cpu_cores, memory, storage):
    # simple random scheduler, without checking avail ressources
    return Node.objects.order_by('?')[0]
    
    # no resources avail:
    return None
