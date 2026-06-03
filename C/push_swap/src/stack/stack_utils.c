/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:28:40 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/10 20:00:15 by mel-shdo         ###   ########.fr       */
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

void	free_stack(t_stack **stack)
{
	t_stack	*temp;

	if (!stack || !*stack)
		return ;
	while (*stack)
	{
		temp = (*stack)->next;
		free(*stack);
		*stack = temp;
	}
	*stack = NULL;
}

int	is_sorted(t_stack *stack)
{
	if (!stack)
		return 1;
	while (stack && stack->next)
	{
		if (stack->content > stack->next->content)
			return (0);
		stack = stack->next;
	}
	return (1);
}

int	find_min(t_stack *stack)
{
	int	min;

	if (!stack)
		return (0);
	min = stack->content;
	while (stack)
	{
		if (min > stack->content)
			min = stack->content;
		stack = stack->next;
	}
	return (min);
}

int	find_max(t_stack *stack)
{
	int	max;
	
	if (!stack)
		return (0);
	max = stack->content;
	while (stack)
	{
		if (max < stack->content)
			max = stack->content;
		stack = stack->next;
	}
	return (max);
}
