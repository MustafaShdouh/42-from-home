/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:28:40 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 20:06:04 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_size(t_stack *stack)
{
	//returns number of elements in stack
}

//free_stack needs to modify the stack so we send **stack to it to prevent dangling pointer
void free_stack(t_stack **stack)
{
	//free the stack and set pointers to NULL
}

int	is_sorted(t_stack *stack)
{
	//checks if the stack is sorted
}

t_stack *find_min(t_stack *stack)
{
	//returns node with the smallest number
}

t_stack *find_max(t_stack *stack)
{
	//returns node with the biggest number
}