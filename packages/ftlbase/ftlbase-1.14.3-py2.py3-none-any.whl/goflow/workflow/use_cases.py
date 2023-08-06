import mutations.fields
from goflow.runtime.models import WorkItem
from goflow.workflow.models import Transition

# Todos os Use Cases de Workflow

TupleField = mutations.fields.build_field_for("TupleField", tuple)
WorkItemField = mutations.fields.build_field_for("WorkItemField", WorkItem)
TransitionField = mutations.fields.build_field_for("TransitionField", Transition)


# class CustomValidator(ValidatorBase):
#     def __init__(self, func, *args, **kwargs):
#         self.func = func
#         super().__init__(*args, **kwargs)
#
#     def is_valid(self, *args, **kwargs):
#         return self.func(*args, **kwargs)


def set_mutation_workitem_status(mutation, activity, default=None):
    """ Se numa mutação de Use Case de WorkFlow o status não é informado e há workflow associado,
        então tenta o status da activity associada ao workitem """
    # Se tem status e workitem, tenta fazer a atualização do status de acordo com a Activity
    if not mutation.status and activity:
        if activity.state_update and activity.state_new:
            mutation.status = activity.state_new
    # Se o status ainda é None, então usar o default ou dá erro
    if not mutation.status:
        if default:
            mutation.status = default
        else:
            s = 'Não foi informado o Status do {mutation} ou a activity {activity}'.format(mutation=mutation,
                                                                                           activity=activity)
            raise mutations.ValidationError(mutation.name, s)


def object_status_update(obj, status, save):
    if obj.status != status:
        obj.status = status
        if save:
            obj.save(update_fields=['status'])
            # obj.save()
    return obj
