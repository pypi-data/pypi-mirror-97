// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';
import { MitoAPI } from '../../../../api';
import { ColumnType } from '../../../Mito';
import { FilterGroupType, FilterType, isFilterGroup, Operator } from './filterTypes';
import { getEmptyFilterData } from './utils';
import { Filter } from './Filter';
import FilterGroup from './FilterGroup';
import { CONDITIONS_WITH_NO_INPUT } from './filterConditions';

import '../../../../../css/filter-card.css';
import '../../../../../css/margins.css';

interface FilterCardProps {
    filters: (FilterType | FilterGroupType)[];
    operator: Operator;

    selectedSheetIndex: number;
    columnHeader: string;
    columnType: ColumnType;

    mitoAPI: MitoAPI;
}

const ADD_FILTER_SELECT_TITLE = '+ Add Filter'

interface FilterCardState {
    /* 
        Filters is a list. Each element of the list is either a filter
        itself, or is a grouping of filters. A grouping of filters is
        a list of filters and an operator.
        
        They are displayed by the filter card in the order they appear
        in the list, and are combined by the operator given in the 
        props.
    */
    filters: (FilterType | FilterGroupType)[];
    operator: Operator;
    stepID: string;
    /* 
        We just store this in state so that we can refresh the select
        so that it is always displayed as the option in the select that is selected
    */
    filterSelect: string;
}


/* 
    Component that contains all that one needs to filter!
*/
class FilterCard extends React.Component<FilterCardProps, FilterCardState> {

    constructor(props: FilterCardProps) {
        super(props);

        this.state = {
            filters: props.filters,
            operator: props.operator,
            stepID: '',
            filterSelect: ADD_FILTER_SELECT_TITLE
        }

        this.sendFilterUpdateMessage = this.sendFilterUpdateMessage.bind(this);
        this.addFilter = this.addFilter.bind(this);
        this.addFilterGroup = this.addFilterGroup.bind(this);
        this.addFilterToGroup = this.addFilterToGroup.bind(this);
        this.deleteFilter = this.deleteFilter.bind(this);
        this.deleteFilterFromGroup = this.deleteFilterFromGroup.bind(this);
        this.setFilter = this.setFilter.bind(this);
        this.setFilterInGroup = this.setFilterInGroup.bind(this);
        this.setOperator = this.setOperator.bind(this);
        this.setOperatorInGroup = this.setOperatorInGroup.bind(this);
    }

    /* 
        Before sending the displayed filters, we parse all the number filters from strings
        to numbers, and then filter out all of the invalid filters (as to not cause errors)
    */
    async sendFilterUpdateMessage(): Promise<void> {

        /* 
            A filter is invalid if:
            1. It should have an input, and it does not
            2. It is a number filter with a string input, or with a non-valid number input        
        */
        const isValidFilter = (filter: FilterType): boolean => {
            if (CONDITIONS_WITH_NO_INPUT.includes(filter.condition)) {
                return true;
            }

            if (filter.type === 'number') {
                return typeof filter.value !== 'string' && !isNaN(filter.value);
            }

            if (filter.type === 'string' || filter.type === 'datetime') {
                return filter.value !== '';
            }

            return true;
        }

        /* 
            The frontend stores number filters as strings, and so we parse them to
            numbers before sending them to the backend
        */
        const parseFilter = (filter: FilterType): FilterType => {
            if (filter.type === 'number' && typeof filter.value === 'string') {
                return {
                    type: filter.type,
                    condition: filter.condition,
                    value: parseFloat(filter.value)
                }
            }
            return filter;
        }

        // To handle decimals, we allow decimals to be submitted, and then just
        // parse them before they are sent to the back-end
        const parsedFilters: (FilterType | FilterGroupType)[] = this.state.filters.map((filterOrGroup): FilterType | FilterGroupType => {
            if (isFilterGroup(filterOrGroup)) {
                return {
                    filters: filterOrGroup.filters.map((filter) => {
                        return parseFilter(filter);
                    }),
                    operator: filterOrGroup.operator
                }
            } else {
                return parseFilter(filterOrGroup)
            }
        })

        const filtersToApply: (FilterType | FilterGroupType)[] = parsedFilters.map((filterOrGroup): FilterType | FilterGroupType => {
            // Filter out these incomplete filters from the group
            if (isFilterGroup(filterOrGroup)) {
                return {
                    filters: filterOrGroup.filters.filter((filter) => {
                        return isValidFilter(filter)
                    }),
                    operator: filterOrGroup.operator
                }
            } else {
                return filterOrGroup
            }
        }).filter((filterOrGroup) => {
            // Filter out the groups if they have no valid filters in them
            if (isFilterGroup(filterOrGroup)) {
                return filterOrGroup.filters.length > 0;
            }
            // And then we filter the non group filters to be non-empty
            return isValidFilter(filterOrGroup)
        });

        const stepID = await this.props.mitoAPI.sendFilterMessage(
            this.props.selectedSheetIndex,
            this.props.columnHeader,
            filtersToApply,
            this.state.operator,
            this.state.stepID
        )

        this.setState({stepID: stepID});
    }

    /* 
        Adds a new, blank filter to the end of the filters list
    */
    addFilter(): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            newFilters.push(
                getEmptyFilterData(this.props.columnType)
            )
            return {
                filters: newFilters
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /* 
        Creates a new filter group (at the bottom) with a single empty
        filter
    */
    addFilterGroup(): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            newFilters.push(
                {
                    filters: [
                        getEmptyFilterData(this.props.columnType)
                    ],
                    operator: 'And'
                }
            )
            return {
                filters: newFilters
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /* 
        Adds a blank new filter to the end of a specific group
    */
    addFilterToGroup(groupIndex: number): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            const filterGroup = newFilters[groupIndex];
            if (isFilterGroup(filterGroup)) {
                // If we do have a filter group at that groupIndex, then we add a new filter to it
                filterGroup.filters.push(
                    getEmptyFilterData(this.props.columnType)
                );
                return {
                    filters: newFilters
                }
            } else {
                // We make no changes if this was not a filter group, which should never occur
                return null;
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /* 
        Deletes a filter that is at the given index in the main
        filter list.
    */
    deleteFilter(filterIndex: number): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            newFilters.splice(filterIndex, 1)
            return {
                filters: newFilters
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /* 
        Deletes a filter that is at a given index in filter list
        of a specific filter group
    */
    deleteFilterFromGroup(groupIndex: number, filterIndex: number): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            const filterGroup = newFilters[groupIndex];
            if (isFilterGroup(filterGroup)) {
                // If we do have a filter group at that groupIndex, then we delete the filter
                // at the passed filterIndex
                filterGroup.filters.splice(filterIndex, 1);  
                
                // If there are no filters left in this group, then we remove the entire group
                if (filterGroup.filters.length === 0) {
                    newFilters.splice(groupIndex, 1);
                }
                
                return {
                    filters: newFilters
                }
            } else {
                // We make no changes if this was not a filter group, which should never occur
                return null;
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /*
        Sets a filter at the given index to the new filter value
    */
    setFilter(filterIndex: number, filter: FilterType): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            newFilters[filterIndex] = filter;
            return {
                filters: newFilters
            };
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    /*
        Sets a filter at the given filterIndex in the specific group at the given
        groupIndex to the new filter value
    */
    setFilterInGroup(groupIndex: number, filterIndex: number, filter: FilterType): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            const filterGroup = newFilters[groupIndex];
            if (isFilterGroup(filterGroup)) {
                filterGroup.filters[filterIndex] = filter;
                return {
                    filters: newFilters
                }
            } else {
                // We make no changes if this was not a filter group, which should never occur
                return null;
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }


    /*
        Sets the operator that combines the highest level filters and
        filter groups
    */
    setOperator(operator: Operator): void {
        this.setState({operator: operator}, () => {
            void this.sendFilterUpdateMessage();
        })
    }

    /*
        Sets the operator that combines a specific filter group
    */
    setOperatorInGroup(groupIndex: number, operator: Operator): void {
        this.setState(prevState => {
            const newFilters = [...prevState.filters];
            const filterGroup = newFilters[groupIndex];
            if (isFilterGroup(filterGroup)) {
                filterGroup.operator = operator;
                return {
                    filters: newFilters
                }
            } else {
                // We make no changes if this was not a filter group, which should never occur
                return null;
            }
        }, () => {
            void this.sendFilterUpdateMessage();
        });
    }

    render(): JSX.Element {
        return (
            <div>
                <div className='filter-modal-section-title mt-25px'>
                    <p> Filter </p>
                </div>
                <div className="filter-modal-centering-container">
                    {this.state.filters.map((filterOrGroup, index) => {
                        if (isFilterGroup(filterOrGroup)) {
                            return (
                                /* 
                                    If the FilterGroup is the first Filter or FilterGroup
                                    in the FilterCard, add a 'Where'
                                */
                                <div className='filter-group-and-operator-div'>
                                    {index === 0 &&
                                        <div className='filter-where-label filter-object-item mr-10px'>
                                            Where
                                        </div>
                                    }
                                    {index !== 0 && 
                                        <div className='filter-select filter-operator mr-10px'>
                                            <select
                                                className='filter-select filter-operator mr-10px'
                                                value={this.state.operator}
                                                onChange={(e) => {this.setOperator(e.target.value as Operator)}}
                                            >
                                                <option value='And'>And</option>
                                                <option value='Or'>Or</option>
                                            </select>
                                        </div>
                                    }
                                    <FilterGroup
                                        key={index}
                                        mainOperator={this.state.operator}
                                        filters={filterOrGroup.filters}
                                        groupOperator={filterOrGroup.operator}
                                        setFilter={(filterIndex, newFilter) => {
                                            this.setFilterInGroup(index, filterIndex, newFilter);
                                        }}
                                        setOperator={(newOperator) => {
                                            this.setOperatorInGroup(index, newOperator);
                                        }}
                                        deleteFilter={(filterIndex: number) => {
                                            this.deleteFilterFromGroup(index, filterIndex);
                                        }}
                                        addFilter={() => this.addFilterToGroup(index)}
                                    />
                                </div>
                                
                            );
                        } else {
                            return (
                                <Filter
                                    first={index === 0}
                                    key={index}
                                    filter={filterOrGroup}
                                    operator={this.state.operator}
                                    displayOperator
                                    setFilter={(newFilter) => {
                                        this.setFilter(index, newFilter)
                                    }}
                                    setOperator={this.setOperator}
                                    deleteFilter={() => {this.deleteFilter(index)}}
                                />
                            );
                        }
                    }
                    )}
                </div>
                <div className='filter-card-buttons-container'>
                    <select 
                        className='filter-add-filter-button'
                        value={ADD_FILTER_SELECT_TITLE}
                        onChange={(e) => {
                            if (e.target.value === 'filter') {
                                this.addFilter()
                            } else {
                                this.addFilterGroup()
                            }
                            // Set this so it's always what is selected
                            this.setState({filterSelect: ADD_FILTER_SELECT_TITLE})
                        }}
                    >
                        <option selected hidden>{ADD_FILTER_SELECT_TITLE}</option>
                        <option value='filter'>+ Add a Filter</option>
                        <option value='filter-group'>+ Add a group of filters</option>
                    </select>
                </div>
            </div>
        )
    }
}

export default FilterCard;