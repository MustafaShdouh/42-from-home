/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 19:14:09 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 20:54:39 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void rotate_stack(t_stack **s)
{
	t_stack	*tail;
	t_stack	*head;

	if (!s || !*s || !(*s)->next)
		return ;
	head = *s;
	tail = stack_last(*s);
	*s = head->next;
	(*s)->prev = NULL;
	tail->next = head;
	head->prev = tail;
	head->next = NULL;
}

void	ra(t_stack **a)
{
	rotate_stack(a);
	write(1, "ra\n", 3);
}

void	rb(t_stack **b)
{
	rotate_stack(b);
	write(1, "rb\n", 3);
}

void	rr(t_stack **a, t_stack **b)
{
	rotate_stack(a);
	rotate_stack(b);
	write(1, "rr\n", 3);
}