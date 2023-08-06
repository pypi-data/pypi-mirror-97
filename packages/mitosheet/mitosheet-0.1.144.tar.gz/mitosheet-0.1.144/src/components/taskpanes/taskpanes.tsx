// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

/* 
    Each Taskpane has a type (included TaskpaneType.NONE, which is the type of _no taskpane_ (e.g. nothing is displayed)).

    If you want to be able to open a taskpane in Mito, then you need to add the type of this taskpane, 
    as well as any parameters it has, to this type.

    For example, if you create a new taskpane 'Dork' that takes a columnHeader as input, then you should
    add a new element here that looks like:
        | {type: 'TaskpaneType.DORK', columnHeader: string}
*/
export enum TaskpaneType {
    NONE = 'none',
    PIVOT = 'pivot',
    MERGE = 'merge',
    STEPS = 'steps',
    DOCUMENTATION = 'documentation',
    CONTROL_PANEL = 'control_panel',
    REPLAY_ANALYSIS = 'replay_analysis'
}

export type TaskpaneInfo = 
    | {type: TaskpaneType.NONE}
    | {type: TaskpaneType.PIVOT} 
    | {type: TaskpaneType.MERGE}
    | {type: TaskpaneType.STEPS}
    | {type: TaskpaneType.DOCUMENTATION}
    | {type: TaskpaneType.CONTROL_PANEL, columnHeader: string, openEditingColumnHeader: boolean}
    | {type: TaskpaneType.REPLAY_ANALYSIS}

/*
    EDITING_TASKPANES are taskpanes that live update edit the sheet using overwrite=True and therefore should be closed
    when the user begins editing the sheet through some other method. 

    EDITING_TASKPANES include: pivot and merge
*/ 
export const EDITING_TASKPANES: TaskpaneType[] = [TaskpaneType.PIVOT, TaskpaneType.MERGE]