/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:28:40 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 21:21:13 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	stack_size(t_stack *stack)
{
	int	count;

	count = 0;
	while (stack != NULL)
	{
		stack = stack->next;
		count++;
	}
	return (count);
}

//free_stack needs to modify the stack so we send **stack to it to prevent dangling pointer
void free_stack(t_stack **stack)
{
	t_stack	*temp;
	t_stack	*current;

	if (!stack || !*stack)
		return ;
	current = *stack;
	while (current)
	{
		temp = current->next;
		free(current);
		current = temp;
	}
	*stack = NULL;
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