
export enum StepType {
    Initialize = 'initialize',
    AddColumn = "add_column",
    DeleteColumn = "delete_column",
    RenameColumn = "rename_column",
    ReorderColumn = "reorder_column",
    FilterColumn = 'filter_column',
    SetColumnFormula = "set_column_formula",
    DataframeDelete = 'dataframe_delete',
    DataframeDuplicate = 'dataframe_duplicate',
    DataframeRename = 'dataframe_rename',
    SimpleImport = 'simple_import',
    RawPythonImport = 'raw_python_import',
    Sort = 'sort',
    Pivot = 'pivot',
    Merge = 'merge'
}


export interface StepData {
    step_id: string;
    step_idx: number;
    step_type: StepType;
    step_display_name: string;
    step_description: string;
    // TODO: in the future, we should extend the StepData interface for
    // each of the different steps, and type these more strongly!
    // Currently, we aren't sending this data!
    params?: Record<string, unknown>; 
}
